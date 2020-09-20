import logging
import sys
import time

import talib
from openpyxl import Workbook
from pandas import np
import matplotlib.pyplot as plt
from pprint import pprint
from data_source.huobi.static_data_source.huobi_4hour_data_source import Huobi4HourData
from data_source.kline_adapter_huobi import KLineAdapterHuobi
from global_data.system import set_system_running, get_system_running, set_margin
from model.ma_table import MaTable
from model.organized import Organized
from control.strategy1 import Strategy1

from data_source.huobi.HuobiDMService import HuobiDM
from data_source.huobi.ReliableHuobiDMService import ReliableHuobiDM
from data_source.huobi.ReliableHuobiDMService import ReturnUtil as ru
from data_source.huobi.helpers.contract_position_info_helper import ContractPositionInfoHelper as cpi_helper
from data_source.huobi.helpers.contract_openorders_helper import ContractOpenOrdersHelper as coo_helper
from data_source.huobi.helpers.contract_trigger_openorders_helper import ContractTriggerOpenOrdersHelper as ctoo_helper
from utils.config_helper import ConfigHelper, ConfigData
from utils.register import Register

logging.basicConfig(level=logging.DEBUG,  # 控制台打印的日志级别
                    filename='qds.log',
                    filemode='w',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    # a是追加模式，默认如果不写的话，就是追加模式
                    format='%(asctime)s : %(message)s'
                    # '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    # 日志格式
                    )

# https://docs.huobigroup.com/docs/dm/v1/cn/#8664ee712b
URL = 'https://api.btcgateway.pro'


file = 'config.xml'
config_helper = ConfigHelper(file)
config = ConfigData()
ret = config_helper.init_root()
if ret:
    config_helper.parse(config)
else:
    logging.debug("Error, please check file {0}".format(file))
    sys.exit(-1)

ACCESS_KEY = config._access_key
SECRET_KEY = config._secret_key

dm = ReliableHuobiDM(URL, ACCESS_KEY, SECRET_KEY)

# 1min, 5min, 15min, 30min, 60min,4hour,1day, 1mon
period = config._period
# ma快线周期
ma_fast = int(config._ema_fast)
# ma慢线周期
ma_slow = int(config._ema_slow)
# 盈利点数
stop_offset = int(config._stop_earning_offset)
# 开仓距离ma_slow的点位数，如果要在ma_slow处建仓应该设置为0
open_offset = int(config._open_offset)
# 分批建仓间隔点位数，如果要一次建仓，应该设置为0
open_interval = int(config._open_interval)
# 杠杆倍数
level_rate = int(config._level_rate)
# 最大开仓数量
max_open_number = int(config._max_open_number)
# 目前只支持BTC当季合约
symbol_type = 'BTC'
symbol_period = 'BTC_CQ'
contract_type_period = 'quarter'

# 行情历史
trend_history = None


def qds_test_registration():
    register_info = Register.get_register_info()
    if register_info != config._qds_id:
        logging.debug("qds_test_registration failed")
        return False
    logging.debug("qds_test_registration ok")
    return True


def qds_test_authorize():
    ret = dm.get_contract_account_position_info(symbol_type)
    if not ru.is_ok(ret):
        logging.debug("qds_test_authorize failed")
        return False
    else:
        logging.debug("qds_test_authorize ok")
        return True


def debug_ema(org_data=Organized()):
    count = 0
    for i in range(0, org_data.GetLen()):
        ema_fast = org_data.ema_list[ma_fast][i]
        ema_slow = org_data.ema_list[ma_slow][i]
        if ema_fast == ema_slow:
            count += 1
            print("ema[{0}]={1} == ema[{2}]={3}".format(ma_fast, ema_fast, ma_slow, ema_slow))
    print("totally {0}".format(count))


def cancell_all_contract():
    ret = dm.cancel_all_contract_order(symbol_type)
    if ru.is_ok(ret):
        logging.debug("cancel_all_contract_order successfully")
    else:
        logging.debug("cancel_all_contract_order failed")

    ret = dm.cancel_all_contract_trigger(symbol_type)
    if ru.is_ok(ret):
        logging.debug("cancel_all_contract_trigger successfully")
    else:
        logging.debug("cancel_all_contract_trigger failed")


def close_all_contract():
    ret = dm.get_contract_position_info(symbol_type)
    if not ru.is_ok(ret):
        logging.debug("close_all_contract get_contract_position_info failed")
        return False
    buy_count = int(cpi_helper.get_orders_count('buy', ret))
    sell_count = int(cpi_helper.get_orders_count('sell', ret))

    if buy_count > 0:
        ret = dm.send_lightning_close_position(symbol_type, contract_type_period, '',
                                               buy_count,
                                               "sell",
                                               '', None)
        if ru.is_ok(ret):
            logging.debug("close_all_contract send_lightning_close_position successfully, direction={0}, volume={1}".format(
                "sell", buy_count))
        else:
            logging.debug("close_all_contract send_lightning_close_position failed, direction={0}, volume={1}".format(
                "sell", buy_count))
    if sell_count > 0:
        ret = dm.send_lightning_close_position(symbol_type, contract_type_period, '',
                                               sell_count,
                                               "buy",
                                               '', None)
        if ru.is_ok(ret):
            logging.debug("close_all_contract send_lightning_close_position successfully, direction={0}, volume={1}".format(
                "buy", sell_count))
        else:
            logging.debug("close_all_contract send_lightning_close_position failed, direction={0}, volume={1}".format(
                "buy", sell_count))


# 解决一个竞争问题，当获取持仓信息，限价挂单数量，触发挂单数量的时候，同时有挂单成交，造成一些数据不匹配
g_fix_race_check_one_more_time = False
# holding 持仓， pending 挂单
def run():
    """
    * 如果趋势发生变化，撤销所有的限价挂单以及委托挂单
    * 如果有逆势持仓，则平掉所有逆势持仓
    * 如果有逆势限价挂单，则撤销所有逆势限价挂单
    * 如果没有顺势持仓，则（如果没有限价挂单，则按最优价格挂单；如果有限价挂单，检查价位是否合理，如果不合理则撤销重新挂单）
    * 如果有顺势持仓，则只挂止盈委托挂单，在慢速ema价格上设置止盈点
    """
    ret = qds_test_registration()
    if not ret:
        logging.debug("Error, software is not correctly registered. Please contact 313970187@qq.com to register")
        return False

    global period
    global ma_fast
    global ma_slow
    global open_offset
    global open_interval
    global stop_offset
    global level_rate
    global max_open_number
    global trend_history
    global_data = Organized()

    logging.debug("qds params: period={0}, ma_fast={1}, ma_slow={2}, open_offset={3}, open_interval={4}, "
                  "stop_offset={5}, level_rate={6}, max_open_number={7}".format(
        period, ma_fast, ma_slow, open_offset, open_interval, stop_offset, level_rate, max_open_number))

    if not get_system_running(): return False
    ret = dm.get_contract_kline(symbol=symbol_period, period=period, size=ma_slow+5)
    if not ru.is_ok(ret):
        logging.debug("get_contract_kline failed")
        return False
    global_data = KLineAdapterHuobi.ParseData(ret['data'])

    close_list = global_data._close_list
    ma_fast_list = talib.EMA(np.array(close_list), timeperiod=ma_fast)
    ma_slow_list = talib.EMA(np.array(close_list), timeperiod=ma_slow)

    global_data._ema_list[ma_fast] = ma_fast_list
    global_data._ema_list[ma_slow] = ma_slow_list

    # debug_ema(global_data)

    last_index = global_data.GetLen() - 2
    last_ema_fast = global_data.ema_list[ma_fast][last_index]
    last_ema_slow = global_data.ema_list[ma_slow][last_index]
    ts = global_data._timestamp[last_index]

    # 多空决策
    trend = None
    if last_ema_fast > last_ema_slow:
        trend = 'long'
    elif last_ema_fast < last_ema_slow:
        trend = 'short'
    else:  # 趋势不变
        if trend_history:
            trend = trend_history
        else:
            trend = 'long'

    # 趋势发生变化，撤销所有的限价挂单以及委托挂单
    logging.debug("ts:{0} ma{1}:{2}, ma{3}:{4}".format(ts, ma_fast, last_ema_fast, ma_slow, last_ema_slow))
    if trend_history != trend:
        trend_history = trend
        logging.debug(
            "trend={5} last: {4} ma{0}:{1}, ma{2}:{3}".format(ma_fast, last_ema_fast, ma_slow, last_ema_slow, ts,
                                                              trend))
        if not get_system_running(): return False
        ret = dm.cancel_all_contract_order(symbol_type)
        if ru.is_ok(ret):
            logging.debug("cancel_all_contract_order successfully at trend changed")
        else:
            if ru.is_no_order(ret):
                logging.debug("cancel_all_contract_order no orders")
            else:
                logging.debug("cancel_all_contract_order failed at trend changed")
                return False

        if not get_system_running(): return False
        ret = dm.cancel_all_contract_trigger(symbol_type)
        if ru.is_ok(ret):
            logging.debug("cancel_all_contract_trigger successfully at trend changed")
        else:
            if ru.is_no_order(ret):
                logging.debug("cancel_all_contract_trigger no orders")
            else:
                logging.debug("cancel_all_contract_trigger failed at trend changed")
                return False

    if not get_system_running(): return False
    ret = dm.get_contract_account_position_info(symbol_type)
    if ru.is_ok(ret):
        available = ret['data'][0]['margin_available']
        balance = ret['data'][0]['margin_balance']
        logging.debug("margin_available={0}, margin_balance={1}".format(available, balance))
        set_margin(available, balance)
        if available == 0.0 and balance == 0.0:
            logging.debug("no available margin {0}, {1}".format(available, balance))
            return False

    # 获取当前持仓多单数量，空单数量，价格
    if not get_system_running(): return False
    ret = dm.get_contract_position_info(symbol_type)
    if not ru.is_ok(ret):
        logging.debug("get_contract_position_info failed")
        return False
    cpi_helper.log_all_orders("buy", ret)
    cpi_helper.log_all_orders('sell', ret)
    limit_holding_buy_count = cpi_helper.get_orders_count('buy', ret)
    limit_holding_buy_price = cpi_helper.get_price('buy', ret)
    limit_holding_sell_count = cpi_helper.get_orders_count('sell', ret)
    limit_holding_sell_price = cpi_helper.get_price('sell', ret)

    # 获取当前限价挂单的方向以及价格
    if not get_system_running(): return False
    ret = dm.get_contract_open_orders(symbol_type)
    if not ru.is_ok(ret):
        logging.debug("get_contract_open_orders failed")
        return False
    coo_helper.log_all_orders('buy', ret)
    coo_helper.log_all_orders('sell', ret)
    limit_pending_buy_count = coo_helper.get_orders_count('buy', 'open', ret)  # 开仓
    limit_pending_close_sell_count = coo_helper.get_orders_count('sell', 'close', ret)  # 平仓
    limit_pending_sell_count = coo_helper.get_orders_count('sell', 'open', ret)
    limit_pending_close_buy_count = coo_helper.get_orders_count('buy', 'close', ret)
    limit_pending_buy_price_list = coo_helper.get_price('buy', 'open', ret)
    limit_pending_sell_price_list = coo_helper.get_price('sell', 'open', ret)

    # 获取当前委托挂单多单数量，空单数量
    if not get_system_running(): return False
    ret = dm.get_contract_trigger_openorders(symbol_type)
    if not ru.is_ok(ret):
        logging.debug("get_contract_trigger_openorders failed")
        return False
    ctoo_helper.log_all_orders('buy', ret)
    ctoo_helper.log_all_orders('sell', ret)
    trigger_holding_buy_count = ctoo_helper.get_orders_count('buy', 'close', ret)
    trigger_holding_sell_count = ctoo_helper.get_orders_count('sell', 'close', ret)
    # 获取当前委托挂单方向以及价格
    trigger_holding_buy_order_price = round(ctoo_helper.get_order_price('buy', ret))
    trigger_holding_sell_order_price = round(ctoo_helper.get_order_price('sell', ret))

    # 设置最大允许操作数量(挂单数量+持仓数量)
    max_on_trend_count = max_open_number

    # 计算当前是否有逆势持仓
    limit_holding_against_trend_count = 0
    limit_holding_against_trend_close_direction = ''
    limit_holding_price = 0
    trigger_holding_against_trend_count = 0
    # 止盈止损
    stop_earning_trigger_type = ''
    stop_earning_trigger_price = 0
    stop_earning_order_price = 0
    stop_earning_direction = ''
    limit_pending_on_trend_count = 0
    limit_pending_close_on_trend_count = 0
    limit_pending_against_trend_count = 0
    limit_pending_on_trend_price_list = []
    trigger_holding_on_trend_order_price = 0
    base_open_point = 0
    if trend == 'long':
        base_open_point = last_ema_slow - open_offset
        limit_holding_against_trend_count = limit_holding_sell_count
        limit_holding_against_trend_close_direction = 'buy'
        trigger_holding_against_trend_count = trigger_holding_sell_count
        trigger_holding_on_trend_count = trigger_holding_sell_count
        trigger_holding_on_trend_order_price = trigger_holding_sell_order_price

        limit_pending_on_trend_open_direction = 'buy'
        limit_pending_on_trend_count = limit_pending_buy_count
        limit_pending_close_on_trend_count = limit_pending_close_sell_count
        limit_pending_against_trend_count = limit_pending_sell_count
        limit_pending_on_trend_price_list = limit_pending_buy_price_list

        limit_holding_on_trend_count = limit_holding_buy_count
        limit_holding_price = limit_holding_buy_price
        stop_earning_trigger_type = 'ge'
        stop_earning_order_price = round(last_ema_slow + stop_offset)
        stop_earning_trigger_price = round(stop_earning_order_price - 10)
        stop_earning_direction = 'sell'
    else:
        base_open_point = last_ema_slow + open_offset
        limit_holding_against_trend_count = limit_holding_buy_count
        limit_holding_against_trend_close_direction = 'sell'
        trigger_holding_against_trend_count = trigger_holding_buy_count
        trigger_holding_on_trend_count = trigger_holding_buy_count
        trigger_holding_on_trend_order_price = trigger_holding_buy_order_price

        limit_pending_on_trend_open_direction = 'sell'
        limit_pending_on_trend_count = limit_pending_sell_count
        limit_pending_close_on_trend_count = limit_pending_close_buy_count
        limit_pending_against_trend_count = limit_pending_buy_count
        limit_pending_on_trend_price_list = limit_pending_sell_price_list

        limit_holding_on_trend_count = limit_holding_sell_count
        limit_holding_price = limit_holding_sell_price
        stop_earning_trigger_type = 'le'
        stop_earning_order_price = round(last_ema_slow - stop_offset)
        stop_earning_trigger_price = round(stop_earning_order_price + 10)
        stop_earning_direction = 'buy'

    # 最优限价挂单价格
    limit_best_price = [
        round(base_open_point - open_interval),
        round(base_open_point),
        round(base_open_point + open_interval)
    ]
    logging.debug("limit_best_price={0}, {1}, {2}".format(limit_best_price[0], limit_best_price[1], limit_best_price[2]))
    # 执行交易
    # 平掉所有逆势持仓
    if limit_holding_against_trend_count > 0:
        logging.debug("limit_holding_against_trend_count={0}".format(limit_holding_against_trend_count))
        if not get_system_running(): return False
        ret = dm.send_lightning_close_position(symbol_type, contract_type_period, '',
                                               int(limit_holding_against_trend_count),
                                               limit_holding_against_trend_close_direction,
                                               '', None)
        if ru.is_ok(ret):
            limit_holding_against_trend_count = 0
            logging.debug("send_lightning_close_position successfully, direction={0}, volume={1}".format(
                limit_holding_against_trend_close_direction, limit_holding_against_trend_count))
        else:
            logging.debug("send_lightning_close_position failed")
            return False

    # 撤销所有逆势限价挂单，简化操作，只要逆势挂单就撤销所有限价挂单
    if limit_pending_against_trend_count > 0:
        logging.debug("limit_pending_against_trend_count={0}".format(limit_pending_against_trend_count))
        if not get_system_running(): return False
        ret = dm.cancel_all_contract_order(symbol_type)
        if ru.is_ok(ret):
            limit_pending_on_trend_count = 0
            limit_pending_against_trend_count = 0
            logging.debug("cancel_all_contract_order successfully")
        else:
            logging.debug("cancel_all_contract_order failed")
            return False

    # 如果没有顺势持仓，则（如果没有限价挂单，则按最优价格挂单；如果有限价挂单，检查价位是否合理，如果不合理则撤销重新挂单）
    if limit_holding_on_trend_count == 0:
        if limit_pending_on_trend_count == 0:
            available_limit_pending_on_trend_count = max_on_trend_count
            logging.debug("available_limit_pending_on_trend_count={0}".format(available_limit_pending_on_trend_count))
            if available_limit_pending_on_trend_count > 0:
                available_limit_pending_on_trend_count_each = [
                    round(available_limit_pending_on_trend_count / 3),
                    round(available_limit_pending_on_trend_count / 3),
                    max_on_trend_count - round(available_limit_pending_on_trend_count / 3) * 2
                ]
                for i in range(0, len(available_limit_pending_on_trend_count_each)):
                    if limit_holding_on_trend_count < max_on_trend_count:
                        price = round(limit_best_price[i])
                        volume = available_limit_pending_on_trend_count_each[i]
                        if volume > available_limit_pending_on_trend_count:
                            volume = available_limit_pending_on_trend_count
                        direction = limit_pending_on_trend_open_direction
                        if price > 0 and volume > 0:
                            if not get_system_running(): return False
                            ret = dm.send_contract_order(symbol=symbol_type, contract_type=contract_type_period, contract_code='',
                                                         client_order_id='', price=price, volume=int(volume),
                                                         direction=direction, offset='open', lever_rate=level_rate,
                                                         order_price_type='limit')
                            if ru.is_ok(ret):
                                available_limit_pending_on_trend_count -= volume
                                logging.debug(
                                    "send_contract_order successfully, price={0} volume={1} direction={2}".format(
                                        price, int(volume), direction))
                            else:
                                logging.debug("send_contract_order failed")
                                return False
        elif limit_pending_on_trend_count != max_on_trend_count:
            global g_fix_race_check_one_more_time
            if limit_pending_on_trend_count < max_on_trend_count and not g_fix_race_check_one_more_time:
                logging.debug(
                    "Fix race issue: limit_pending_on_trend_count {0} is smaller than max_on_trend_count {1}, "
                    "need to check one more time".format(limit_pending_on_trend_count, max_on_trend_count))
                g_fix_race_check_one_more_time = True
            else:
                g_fix_race_check_one_more_time = False
                if not get_system_running(): return False
                ret = dm.cancel_all_contract_order(symbol_type)
                if ru.is_ok(ret):
                    logging.debug(
                        "cancel_all_contract_order successfully, limit_pending_on_trend_count {0} not match with "
                        "max_on_trend_count {1}".format(limit_pending_on_trend_count, max_on_trend_count))
                else:
                    logging.debug("cancel_all_contract_order failed")
                    return False
        else:
            logging.debug("limit_pending_on_trend_count={0}".format(limit_pending_on_trend_count))
            for i in range(0, len(limit_pending_on_trend_price_list)):
                price = limit_pending_on_trend_price_list[i]
                # 如果限价挂单价格不是最优价格，则撤销重新挂单
                is_best_limit_price = False
                for j in range(0, len(limit_best_price)):
                    if price == limit_best_price[j]:
                        is_best_limit_price = True
                if not is_best_limit_price:
                    if not get_system_running(): return False
                    ret = dm.cancel_all_contract_order(symbol_type)
                    if ru.is_ok(ret):
                        logging.debug(
                            "cancel_all_contract_order successfully, price={0} is not one of limit_best_price".format(
                                price))
                    else:
                        logging.debug("cancel_all_contract_order failed")
                        return False
                    break

    # 如果有顺势持仓，则只挂止盈委托挂单，在持仓的价格上设置止盈点
    # 在只有限价单持仓的情况下，才能设置止盈委托挂单，否则会容易交易失败，而且不合逻辑
    available_trigger_pending_on_trend_count = limit_holding_on_trend_count - \
                                               limit_pending_close_on_trend_count - trigger_holding_on_trend_count
    if available_trigger_pending_on_trend_count > 0:
        logging.debug("available_trigger_pending_on_trend_count={0}".format(available_trigger_pending_on_trend_count))
        if not get_system_running(): return False
        ret = dm.send_contract_trigger_order(symbol=symbol_type, contract_type=contract_type_period,
                                             contract_code=None,
                                             trigger_type=stop_earning_trigger_type,
                                             trigger_price=round(stop_earning_trigger_price),
                                             order_price=round(stop_earning_order_price),
                                             order_price_type='limit',
                                             volume=int(available_trigger_pending_on_trend_count),
                                             direction=stop_earning_direction,
                                             offset='close',
                                             lever_rate=level_rate)
        if ru.is_ok(ret):
            logging.debug("send_contract_trigger_order successfully, {0} {1} {2} {3} {4}".format(
                stop_earning_trigger_type, round(stop_earning_trigger_price), round(stop_earning_order_price),
                int(available_trigger_pending_on_trend_count), stop_earning_direction))
        else:
            logging.debug("send_contract_trigger_order failed")
            return False


run_business_enabled = False


def set_buniness_enabled(enabled):
    global run_business_enabled
    global trend_history

    run_business_enabled = enabled
    if not enabled:
        trend_history = None


def get_business_enabled():
    global run_business_enabled
    return run_business_enabled


def run_business(p=None, mf=None, ms=None, oo=None, oi=None, so=None, lr=None, mn=None):
    global period
    global level_rate
    global ma_fast
    global ma_slow
    global open_offset
    global open_interval
    global stop_offset
    global max_open_number
    global run_business_enabled

    period = p
    ma_fast = int(mf)
    ma_slow = int(ms)
    open_offset = int(oo)
    open_interval = int(oi)
    stop_offset = int(so)
    level_rate = int(lr)
    max_open_number = int(mn)

    if run_business_enabled:
        return run()


if __name__ == "__main__":
    run_count = 0

    while True:
        logging.debug("run_count={0}".format(run_count))

        try:
            run()
        except Exception as e:
            pass

        time.sleep(60)
        run_count += 1
