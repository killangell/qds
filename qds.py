import logging
import time

import talib
from openpyxl import Workbook
from pandas import np
import matplotlib.pyplot as plt

from data_source.huobi.static_data_source.huobi_4hour_data_source import Huobi4HourData
from data_source.kline_adapter_huobi import KLineAdapterHuobi
from model.ma_table import MaTable
from model.organized import Organized
from control.strategy1 import Strategy1

from data_source.huobi.HuobiDMService import HuobiDM
from data_source.huobi.ReliableHuobiDMService import ReliableHuobiDM
from data_source.huobi.ReliableHuobiDMService import ReturnUtil as ru
from data_source.huobi.helpers.contract_position_info_helper import ContractPositionInfoHelper as cpi_helper
from data_source.huobi.helpers.contract_openorders_helper import ContractOpenOrdersHelper as coo_helper
from data_source.huobi.helpers.contract_trigger_openorders_helper import ContractTriggerOpenOrdersHelper as ctoo_helper

from pprint import pprint

logging.basicConfig(level=logging.DEBUG,  # 控制台打印的日志级别
                    filename='qds.log',
                    filemode='w',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    # a是追加模式，默认如果不写的话，就是追加模式
                    format='%(asctime)s : %(message)s'
                    # '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    # 日志格式
                    )

# https://docs.huobigroup.com/docs/dm/v1/cn/#8664ee712b
#### input huobi dm url
URL = 'https://api.btcgateway.pro'

####  input your access_key and secret_key below:
ACCESS_KEY = '61bf2917-d263b13d-ghxertfvbf-1ebd5'
SECRET_KEY = '8eb611d4-7daf05ac-fc2c15ff-0b1ca'

dm = ReliableHuobiDM(URL, ACCESS_KEY, SECRET_KEY)

trend_history = None


def SaveToFile(file_name, line_data_list):
    wb = Workbook()
    wb.create_sheet("Sheet")
    # create title
    wb['Sheet'].cell(row=1, column=1, value="ma_fast")
    wb['Sheet'].cell(row=1, column=2, value="ma_slow")
    wb['Sheet'].cell(row=1, column=3, value="threshold")
    wb['Sheet'].cell(row=1, column=4, value="profit")
    wb['Sheet'].cell(row=1, column=5, value="number")
    wb['Sheet'].cell(row=1, column=6, value="positive")
    wb['Sheet'].cell(row=1, column=7, value="negative")
    wb['Sheet'].cell(row=1, column=8, value="win")
    wb['Sheet'].cell(row=1, column=9, value="rate")
    row_index = 2
    for line_data in line_data_list:
        wb['Sheet'].cell(row=row_index, column=1, value=line_data._ma_fast)
        wb['Sheet'].cell(row=row_index, column=2, value=line_data._ma_slow)
        wb['Sheet'].cell(row=row_index, column=3, value=line_data._threshold)
        wb['Sheet'].cell(row=row_index, column=4, value=line_data._profit)
        wb['Sheet'].cell(row=row_index, column=5, value=line_data._total_number)
        wb['Sheet'].cell(row=row_index, column=6, value=line_data._positive_number)
        wb['Sheet'].cell(row=row_index, column=7, value=line_data._negative_number)
        wb['Sheet'].cell(row=row_index, column=8, value=line_data._win)
        wb['Sheet'].cell(row=row_index, column=9, value=line_data._rate)
        row_index += 1
    wb.save("{0}.xlsx".format(file_name))


# holding 持仓， pending 挂单
def run2():
    """
    * 如果趋势发生变化，撤销所有的限价挂单以及委托挂单
    * 如果有逆势持仓，则平掉所有逆势持仓
    * 如果有逆势限价挂单，则撤销所有逆势限价挂单
    * 如果没有顺势持仓，则（如果没有限价挂单，则按最优价格挂单；如果有限价挂单，检查价位是否合理，如果不合理则撤销重新挂单）
    * 如果有顺势持仓，则只挂止盈委托挂单，在持仓的价格上设置止盈点
    """
    global trend_history
    global_data = Organized()
    ma_fast = 7
    ma_slow = 30
    # pprint(dm.get_contract_kline(symbol=global_symbol, period='4hour', size=20))
    ret = dm.get_contract_kline(symbol='BTC_NQ', period='4hour', size=100)
    if not ru.is_ok(ret):
        logging.debug("get_contract_kline failed")
        return False
    global_data = KLineAdapterHuobi.ParseData(ret['data'])

    close_list = global_data._close_list
    ma_fast_list = talib.EMA(np.array(close_list), timeperiod=ma_fast)
    ma_slow_list = talib.EMA(np.array(close_list), timeperiod=ma_slow)

    global_data._ema_list[ma_fast] = ma_fast_list
    global_data._ema_list[ma_slow] = ma_slow_list

    last_index = global_data.GetLen() - 2
    last_ema_fast = global_data.ema_list[ma_fast][last_index]
    last_ema_slow = global_data.ema_list[ma_slow][last_index]
    ts = global_data._timestamp[last_index]

    # 多空设置
    trend = ''
    # 获取当前趋势是多还是空
    if last_ema_fast > last_ema_slow:
        trend = 'long'
    else:
        trend = 'short'

    # 趋势发生变化，撤销所有的限价挂单以及委托挂单
    if trend_history != trend:
        trend_history = trend
        logging.debug(
            "trend={5} last: {4} ma{0}:{1}, ma{2}:{3}".format(ma_fast, last_ema_fast, ma_slow, last_ema_slow, ts,
                                                              trend))
        ret = dm.cancel_all_contract_order("BTC")
        if ru.is_ok(ret):
            logging.debug("cancel_all_contract_order successfully at trend changed")
        else:
            logging.debug("cancel_all_contract_order failed at trend changed")

        ret = dm.cancel_all_contract_trigger("BTC")
        if ru.is_ok(ret):
            logging.debug("cancel_all_contract_trigger successfully at trend changed")
        else:
            logging.debug("cancel_all_contract_trigger failed at trend changed")

        ret = dm.get_contract_account_position_info('BTC')
        if ru.is_ok(ret):
            logging.debug("margin_available={0}, margin_balance={1}".format(ret['data'][0]['margin_available'],
                                                                    ret['data'][0]['margin_balance']))

    # 获取当前持仓多单数量，空单数量，价格
    # logging.debug("get_contract_position_info")
    ret = dm.get_contract_position_info("BTC")
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
    # logging.debug("get_contract_open_orders")
    ret = dm.get_contract_open_orders("BTC")
    if not ru.is_ok(ret):
        logging.debug("get_contract_open_orders failed")
        return False
    coo_helper.log_all_orders('buy', ret)
    coo_helper.log_all_orders('sell', ret)
    limit_pending_buy_count = coo_helper.get_orders_count('buy', 'open', ret)
    limit_pending_sell_count = coo_helper.get_orders_count('sell', 'open', ret)
    limit_pending_buy_price_list = coo_helper.get_price('buy', 'open', ret)
    limit_pending_sell_price_list = coo_helper.get_price('sell', 'open', ret)

    # 获取当前委托挂单多单数量，空单数量
    # logging.debug("get_contract_trigger_openorders")
    ret = dm.get_contract_trigger_openorders("BTC")
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
    max_on_trend_count = 3
    # 最优限价挂单价格
    limit_best_price = [round(last_ema_slow - 50), round(last_ema_slow), round(last_ema_slow + 50)]
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
    limit_pending_against_trend_count = 0
    limit_pending_on_trend_price_list = []
    trigger_holding_on_trend_order_price = 0

    if trend == 'long':
        limit_holding_against_trend_count = limit_holding_sell_count
        limit_holding_against_trend_close_direction = 'open'
        trigger_holding_against_trend_count = trigger_holding_sell_count
        trigger_holding_on_trend_count = trigger_holding_sell_count
        trigger_holding_on_trend_order_price = trigger_holding_sell_order_price

        limit_pending_on_trend_open_direction = 'buy'
        limit_pending_on_trend_count = limit_pending_buy_count
        limit_pending_against_trend_count = limit_pending_sell_count
        limit_pending_on_trend_price_list = limit_pending_buy_price_list

        limit_holding_on_trend_count = limit_holding_buy_count
        limit_holding_price = limit_holding_buy_price
        stop_earning_trigger_type = 'ge'
        stop_earning_order_price = round(last_ema_slow + 200)
        stop_earning_trigger_price = round(stop_earning_order_price - 10)
        stop_earning_direction = 'sell'
    else:
        limit_holding_against_trend_count = limit_holding_buy_count
        limit_holding_against_trend_close_direction = 'sell'
        trigger_holding_against_trend_count = trigger_holding_buy_count
        trigger_holding_on_trend_count = trigger_holding_buy_count
        trigger_holding_on_trend_order_price = trigger_holding_buy_order_price

        limit_pending_on_trend_open_direction = 'sell'
        limit_pending_on_trend_count = limit_pending_sell_count
        limit_pending_against_trend_count = limit_pending_buy_count
        limit_pending_on_trend_price_list = limit_pending_sell_price_list

        limit_holding_on_trend_count = limit_holding_sell_count
        limit_holding_price = limit_holding_sell_price
        stop_earning_trigger_type = 'le'
        stop_earning_order_price = round(last_ema_slow - 200)
        stop_earning_trigger_price = round(stop_earning_order_price + 10)
        stop_earning_direction = 'buy'

    # 计算当前是否有逆势限价挂单

    # 执行交易

    # 平掉所有逆势持仓
    if limit_holding_against_trend_count > 0:
        logging.debug("limit_holding_against_trend_count={0}".format(limit_holding_against_trend_count))
        ret = dm.send_lightning_close_position("BTC", "next_quarter", '',
                                               limit_holding_against_trend_count,
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
        ret = dm.cancel_all_contract_order("BTC")
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
                            ret = dm.send_contract_order(symbol='BTC', contract_type='next_quarter', contract_code='',
                                                         client_order_id='', price=price, volume=int(volume),
                                                         direction=direction, offset='open', lever_rate=10,
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
            ret = dm.cancel_all_contract_order('BTC')
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
                    ret = dm.cancel_all_contract_order('BTC')
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
    available_trigger_pending_on_trend_count = limit_holding_on_trend_count - trigger_holding_on_trend_count
    if available_trigger_pending_on_trend_count > 0:
        logging.debug("available_trigger_pending_on_trend_count={0}".format(available_trigger_pending_on_trend_count))
        ret = dm.send_contract_trigger_order(symbol='BTC', contract_type='next_quarter',
                                             contract_code=None,
                                             trigger_type=stop_earning_trigger_type,
                                             trigger_price=round(stop_earning_trigger_price),
                                             order_price=round(stop_earning_order_price),
                                             order_price_type='limit',
                                             volume=int(available_trigger_pending_on_trend_count),
                                             direction=stop_earning_direction,
                                             offset='close',
                                             lever_rate=10)
        if ru.is_ok(ret):
            logging.debug("send_contract_trigger_order successfully, {0} {1} {2} {3} {4}".format(
                stop_earning_trigger_type, round(stop_earning_trigger_price), round(stop_earning_order_price),
                int(available_trigger_pending_on_trend_count), stop_earning_direction))
        else:
            # logging.debug("send_contract_trigger_order failed due to {0}.{1}".format(ret['err_code'], ret['err_msg']))
            logging.debug("send_contract_trigger_order failed")
            return False


if __name__ == "__main__":
    run_count = 0

    while True:
        logging.debug("\n\nrun_count={0}".format(run_count))

        try:
            run2()
        except Exception as e:
            pass

        time.sleep(60)
        run_count += 1
