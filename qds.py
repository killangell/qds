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
def run():
    """
    本量化模型在如下限制下运行，请确保程序运行时，所操作账户没有任何挂单和持仓。
    1. 限价单可以挂多条记录，每条记录可以有不同的价格和不同的数量
    2. 委托单只可以挂一条记录，价格和数量都在这一条记录里，因为委托单只用来设置止盈，止盈的点位一样
    3. 只设置止盈，不设置止损，止损在趋势反转时，直接平仓
    4. 趋势发横变化，撤销所有的限价挂单，只保留顺势限价单持仓
    5. 限价单只用来开仓，委托单只用来平仓
    """
    global trend_history
    global_data = Organized()
    ma_fast = 7
    ma_slow = 30
    # pprint(dm.get_contract_kline(symbol=global_symbol, period='4hour', size=20))
    ret = dm.get_contract_kline(symbol='BTC_NQ', period='4hour', size=100)
    if not ru.is_ok(ret):
        # {'status': 'fail', 'msg': "HTTPSConnectionPool(host='api.btcgateway.pro', port=443): Read timed out. (read timeout=5)"}
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
        logging.debug("trend={5} last: {4} ma{0}:{1}, ma{2}:{3}".format(ma_fast, last_ema_fast, ma_slow, last_ema_slow, ts, trend))
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

    # 获取当前持仓多单数量，空单数量
    logging.debug("get_contract_position_info")
    ret = dm.get_contract_position_info("BTC")
    if not ru.is_ok(ret):
        # logging.debug("get_contract_position_info failed due to {0}.{1}".format(ret['err_code'], ret['err_msg']))
        logging.debug("get_contract_position_info failed")
        return False
    cpi_helper.log_all_orders("buy", ret)
    cpi_helper.log_all_orders('sell', ret)
    limit_holding_buy_count = cpi_helper.get_orders_count('buy', ret)
    limit_holding_sell_count = cpi_helper.get_orders_count('sell', ret)
    # 获取当前持仓方向以及价格

    # 获取当前限价挂单的方向以及价格
    logging.debug("get_contract_open_orders")
    ret = dm.get_contract_open_orders("BTC")
    if not ru.is_ok(ret):
        # logging.debug("get_contract_open_orders failed due to {0}.{1}".format(ret['err_code'], ret['err_msg']))
        logging.debug("get_contract_open_orders failed")
        return False
    coo_helper.log_all_orders('buy', ret)
    coo_helper.log_all_orders('sell', ret)
    limit_pending_buy_count = coo_helper.get_orders_count('buy', ret)
    limit_pending_sell_count = coo_helper.get_orders_count('sell', ret)
    limit_pending_buy_price_list = coo_helper.get_price('buy', ret)
    limit_pending_sell_price_list = coo_helper.get_price('sell', ret)

    # 获取当前委托挂单多单数量，空单数量
    logging.debug("get_contract_trigger_openorders")
    ret = dm.get_contract_trigger_openorders("BTC")
    if not ru.is_ok(ret):
        # {'status': 'fail', 'msg': "HTTPSConnectionPool(host='api.btcgateway.pro', port=443): Read timed out. (read timeout=5)"}
        # logging.debug("get_contract_trigger_openorders failed due to {0}".format(ret['msg']))
        logging.debug("get_contract_trigger_openorders failed")
        return False
    ctoo_helper.log_all_orders('buy', ret)
    ctoo_helper.log_all_orders('sell', ret)
    trigger_holding_buy_count = ctoo_helper.get_orders_count('buy', ret)
    trigger_holding_sell_count = ctoo_helper.get_orders_count('sell', ret)
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
        stop_earning_trigger_type = 'le'
        stop_earning_order_price = round(last_ema_slow - 200)
        stop_earning_trigger_price = round(stop_earning_order_price + 10)
        stop_earning_direction = 'buy'

    # 计算当前是否有逆势限价挂单

    # 执行交易

    # 平掉所有逆势持仓
    logging.debug("limit_holding_against_trend_count={0}".format(limit_holding_against_trend_count))
    if limit_holding_against_trend_count > 0:
        ret = dm.send_lightning_close_position("BTC", "next_quarter", '',
                                               limit_holding_against_trend_count,
                                               limit_holding_against_trend_close_direction,
                                               '', None)
        if ru.is_ok(ret):
            limit_holding_against_trend_count = 0
            logging.debug("send_lightning_close_position successfully, direction={0}, volume={1}".format(
                limit_holding_against_trend_close_direction, limit_holding_against_trend_count))
        else:
            # logging.debug("send_lightning_close_position failed due to {0}.{1}".format(ret['err_code'], ret['err_msg']))
            logging.debug("send_lightning_close_position failed")
            return False

    # 撤销所有逆势限价挂单，简化操作，只要逆势挂单就撤销所有限价挂单
    logging.debug("limit_pending_against_trend_count={0}".format(limit_pending_against_trend_count))
    if limit_pending_against_trend_count > 0:
        ret = dm.cancel_all_contract_order("BTC")
        if ru.is_ok(ret):
            limit_pending_on_trend_count = 0
            limit_pending_against_trend_count = 0
            logging.debug("cancel_all_contract_order successfully")
        else:
            # logging.debug("cancel_all_contract_order failed due to {0}.{1}".format(ret['err_code'], ret['err_msg']))
            logging.debug("cancel_all_contract_order failed")
            return False

    # 如果有顺势挂单，看挂单价格是否合理，不合理的话，撤销重新挂单
    logging.debug("limit_pending_on_trend_count={0}".format(limit_pending_on_trend_count))
    if limit_pending_on_trend_count > 0:
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
                    limit_pending_on_trend_count = 0
                    limit_pending_against_trend_count = 0
                    logging.debug("cancel_all_contract_order successfully, price={0} is not one of limit_best_price".format(
                        price))
                else:
                    # logging.debug("cancel_all_contract_order failed due to {0}.{1}".format(ret['err_code'], ret['err_msg']))
                    logging.debug("cancel_all_contract_order failed")
                    return False

    # 撤销所有逆势委托挂单，简化操作，只要有逆势挂单就撤销所有委托挂单
    # 逆势委托挂单，有可能是止盈止损，所以这部分操作不需要了
    """
    if trigger_holding_against_trend_count > 0:
        ret = dm.cancel_all_contract_trigger("BTC")
        if ru.is_ok(ret):
            trigger_holding_against_trend_count = 0
            trigger_holding_on_trend_count = 0
        else:
            logging.debug("Failed to cancel trigger contract")
            return False
    """

    # 如果当前有顺势持仓的话，检查是否有平仓委托挂单，如果有:
    # 如果价格不合理则撤销重新挂
    # 如果挂单数量与持仓数量不等则重挂
    logging.debug("limit_holding_on_trend_count={0}, limit_pending_on_trend_count={1}, "
                  "trigger_holding_on_trend_count={2}".format(limit_holding_on_trend_count,
                                                              limit_pending_on_trend_count,
                                                              trigger_holding_on_trend_count))
    if limit_holding_on_trend_count > 0 or limit_pending_on_trend_count > 0:
        if trigger_holding_on_trend_count > 0:
            if round(trigger_holding_on_trend_order_price) != round(stop_earning_order_price) or \
                    trigger_holding_on_trend_count > limit_holding_on_trend_count:
                ret = dm.cancel_all_contract_trigger("BTC")
                if ru.is_ok(ret):
                    trigger_holding_on_trend_count = 0
                    logging.debug(
                        "cancel_all_contract_trigger successfully, trigger_order_price={0} stop_earning_order_price={1} limit_holding_on_trend_count={2} trigger_holding_on_trend_count={3}".format(
                            trigger_holding_on_trend_order_price,
                            stop_earning_order_price, limit_holding_on_trend_count, trigger_holding_on_trend_count))
                else:
                    # logging.debug("cancel_all_contract_trigger failed due to {0}.{1}".format(ret['err_code'], ret['err_msg']))
                    logging.debug("cancel_all_contract_trigger failed")
                    return False

    # 检查当前是否有顺势限价挂单，如果有：
    # 价格不合理则撤销重新挂

    # 检查当前是否还需要挂单，如果需要(最大可以交易数量-已经持仓数量>0)则设置限价挂单
    # 挂限价单以及委托挂单
    available_limit_pending_on_trend_count = max_on_trend_count - limit_holding_on_trend_count - limit_pending_on_trend_count
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
                        # 这里不能增加limit_holding_on_trend_count的数量，因为限价挂单成功不代表就能立即成交变为持仓
                        # limit_holding_on_trend_count += volume
                        available_limit_pending_on_trend_count -= volume
                        logging.debug("send_contract_order successfully, price={0} volume={1} direction={2}".format(
                            price, int(volume), direction))
                    else:
                        # logging.debug("send_contract_order failed due to {0}.{1}".format(ret['err_code'], ret['err_msg']))
                        logging.debug("send_contract_order failed")
                        return False

    # 在只有限价单持仓的情况下，才能设置止盈委托挂单，否则会容易交易失败，而且不合逻辑
    available_trigger_pending_on_trend_count = limit_holding_on_trend_count - trigger_holding_on_trend_count
    logging.debug("available_trigger_pending_on_trend_count={0}".format(available_trigger_pending_on_trend_count))
    if available_trigger_pending_on_trend_count > 0:
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
        logging.debug("run_count={0}".format(run_count))

        try:
            run()
        except Exception as e:
            pass

        time.sleep(60*3)
        run_count += 1



    if 0:
        global_data = Organized()
        # data_source = Huobi1HourData.GetTestData_1hour_2000_2()
        data_source = Huobi4HourData.GetTestData_4hour_2000()
        global_data = KLineAdapterHuobi.ParseData(data_source['data'])

        print("totally {0} kline data".format(len(global_data._close_list)))
        ma_table_list = []
        # for ma_fast in range(3, 60):
        #    for ma_slow in range(ma_fast + 1, 90):
        for ma_fast in range(7, 8):
            for ma_slow in range(30, 31):
                close_list = global_data._close_list
                ma_fast_list = talib.EMA(np.array(close_list), timeperiod=ma_fast)
                ma_slow_list = talib.EMA(np.array(close_list), timeperiod=ma_slow)

                global_data._ema_list[ma_fast] = ma_fast_list
                global_data._ema_list[ma_slow] = ma_slow_list

                ma_table = Strategy1.Run(ma_fast, ma_slow, global_data, True)
                ma_table_list.append(ma_table)

        SaveToFile("4hour_2000", ma_table_list)

    if 0:
        global_data = Organized()
        ma_fast = 7
        ma_slow = 30
        # pprint(dm.get_contract_kline(symbol='BTC_NQ', period='4hour', size=20))
        data_source = dm.get_contract_kline(symbol='BTC_NQ', period='4hour', size=100)
        global_data = KLineAdapterHuobi.ParseData(data_source['data'])

        close_list = global_data._close_list
        ma_fast_list = talib.EMA(np.array(close_list), timeperiod=ma_fast)
        ma_slow_list = talib.EMA(np.array(close_list), timeperiod=ma_slow)

        global_data._ema_list[ma_fast] = ma_fast_list
        global_data._ema_list[ma_slow] = ma_slow_list

        ma_table = Strategy1.Run(ma_fast, ma_slow, global_data)
        # SaveToFile(1, ma_table)
        macd, signal, hist = talib.MACD(np.array(close_list), fastperiod=12, slowperiod=26, signalperiod=9)
        global_data._hist_list = hist

        macd_state = 0
        for i in range(0, len(global_data._id_list)):
            ts = global_data._timestamp[i]
            macd = global_data._hist_list[i]
            # print("{0} - {1}".format(ts, macd))
            if macd_state == 0:
                if macd > 0:
                    macd_state = 1
                elif macd < 0:
                    macd_state = -1
            if (macd_state == 1 and macd < 0) or (macd_state == -1 and macd > 0):
                print("{0} - {1}".format(ts, macd))
                if macd > 0:
                    macd_state = 1
                elif macd < 0:
                    macd_state = -1

        # plt.plot(close_list)
        plt.plot(ma_fast_list)
        plt.plot(ma_slow_list)
        plt.grid()
        plt.show()

    """
    if 0:
        global_data = Organized()
        ma_fast = 7
        ma_slow = 30
        # pprint(dm.get_contract_kline(symbol=global_symbol, period='4hour', size=20))
        data_source = dm.get_contract_kline(symbol='BTC_NQ', period='4hour', size=100)
        global_data = KLineAdapterHuobi.ParseData(data_source['data'])

        close_list = global_data._close_list
        ma_fast_list = talib.EMA(np.array(close_list), timeperiod=ma_fast)
        ma_slow_list = talib.EMA(np.array(close_list), timeperiod=ma_slow)

        global_data._ema_list[ma_fast] = ma_fast_list
        global_data._ema_list[ma_slow] = ma_slow_list

        last_index = global_data.GetLen() - 2
        last_ema_fast = global_data.ema_list[ma_fast][last_index]
        last_ema_slow = global_data.ema_list[ma_slow][last_index]
        ts = global_data._timestamp[last_index]
        print("last: {4} ma{0}:{1}, ma{2}:{3}".format(ma_fast, last_ema_fast, ma_slow, last_ema_slow, ts))

        if 1:
            # 应该多还是空
            # last_ema_fast > last_ema_slow: 多
            # last_ema_fast < last_ema_slow: 空
            # 查看持仓

            # 限价持仓多单数量
            limit_hold_buy_count = None
            # 限价持仓空单数量
            limit_hold_sell_count = None
            # 限价挂单多单数量
            limit_to_buy_count = None
            # 限价挂单空单数量
            limit_to_sell_count = None
            # 触发挂单多单数量
            trigger_to_buy_count = None
            # 触发挂单空单数量
            trigger_to_sell_count = None

            # 获取限价持仓信息
            ret = dm.get_contract_position_info("BTC")
            if not ru.is_ok(ret):
                printf("Will continue in next {0} minutes", 5)
            cpi_helper.log_all_orders("buy", ret)
            cpi_helper.log_all_orders('sell', ret)
            limit_hold_buy_count = cpi_helper.get_orders_count('buy', ret)
            limit_hold_sell_count = cpi_helper.get_orders_count('sell', ret)
            # 获取限价挂单信息
            ret = dm.get_contract_open_orders("BTC")
            limit_to_buy_count = coo_helper.get_orders_count('buy', ret)
            limit_to_sell_count = coo_helper.get_orders_count('sell', ret)
            # 获取触发挂单信息
            ret = dm.get_contract_trigger_openorders("BTC")
            trigger_to_buy_count = ctoo_helper.get_orders_count('buy', ret)
            trigger_to_sell_count = ctoo_helper.get_orders_count('sell', ret)
            trigger_buy_order_price = ctoo_helper.get_order_price('buy', ret)
            trigger_sell_order_price = ctoo_helper.get_order_price('sell', ret)

            # 交易趋势
            trend = None
            # 平仓方向
            close_direction = None
            # 交易方向
            open_direction = None
            # 逆趋势，需要平仓的数量
            need_close_contract_count = None
            # 顺趋势，持仓合约的数量
            ongoing_contract_count = None
            # 3档挂单价位
            limit_price = [last_ema_slow - 50, last_ema_slow, last_ema_slow + 50]
            # 止盈价格, 200点止盈
            stop_earning_trigger_type = None
            stop_earning_trigger_price = None
            stop_earning_order_price = None
            stop_earning_direction = None
            is_stop_earning_set = None
            is_stop_earning_price_reasonable = None
            # 触发挂单，当前设置的止盈价格
            trigger_stop_earning_order_price_set = None

            # 量化交易，最大交易的合约张数
            max_contract_count = 3

            # 多空决策
            if last_ema_fast > last_ema_slow:
                trend = 'long'
                close_direction = 'buy'
                open_direction = 'buy'
                need_close_contract_count = limit_hold_sell_count
                ongoing_contract_count = limit_hold_buy_count
                stop_earning_trigger_type = 'ge'
                stop_earning_order_price = last_ema_slow + 200
                stop_earning_trigger_price = stop_earning_order_price - 10
                stop_earning_direction = 'sell'
                trigger_stop_earning_order_price_set = trigger_sell_order_price
                is_stop_earning_set = trigger_to_sell_count > 0
            else:
                trend = 'short'
                close_direction = 'sell'
                open_direction = 'sell'
                need_close_contract_count = limit_hold_buy_count
                ongoing_contract_count = limit_hold_sell_count
                stop_earning_trigger_type = 'le'
                stop_earning_order_price = last_ema_slow - 200
                stop_earning_trigger_price = stop_earning_order_price + 10
                stop_earning_direction = 'buy'
                trigger_stop_earning_order_price_set = trigger_buy_order_price
                is_stop_earning_set = trigger_to_buy_count > 0
            is_stop_earning_price_reasonable = trigger_stop_earning_order_price_set == stop_earning_order_price

            if need_close_contract_count > 0:
                # 执行平仓操作，因为和趋势的方向不同
                bret = dm.reliable_send_lightning_close_position("BTC", "next_quarter", '',
                                                                 need_close_contract_count,
                                                                 close_direction, '', None)
                if not bret:
                    logging.debug("Failed to close direction={0} volume={1}".
                                  format(close_direction, need_close_contract_count))
                    # return False

            # 取消逆势挂单，为简化操作，如果发现两个方向都有挂单，则撤销所有挂单，然后在后面重新挂顺势单
            if (limit_to_buy_count > 0 and limit_to_sell_count > 0) or \
                    (trend == 'long' and limit_to_sell_count > 0) or \
                    (trend == 'short' and limit_to_buy_count > 0):
                ret = dm.cancel_all_contract_order("BTC")
                if ru.is_ok(ret):
                    limit_to_buy_count = 0
                    limit_to_sell_count = 0
                else:
                    logging.debug("Failed to cancel contract")
                    # return False

            if ongoing_contract_count >= max_contract_count:
                logging.debug("Failed to proceed as ongoing contract number:{0} >= max:{1}".
                              format(ongoing_contract_count, max_contract_count))
                # 是否有止盈止损触发挂单，检查价位是否合理，不合理的画，撤销重新设置
                if is_stop_earning_set and (not is_stop_earning_price_reasonable): 
                    # 撤销止盈止损
                # 没有止盈止损，则设置触发挂单，数量等于持仓限价单数量
                else:
                    ret = dm.send_contract_trigger_order(symbol='BTC', contract_type='next_quarter',
                                                         contract_code=None,
                                                         trigger_type=stop_earning_trigger_type,
                                                         trigger_price=stop_earning_trigger_price,
                                                         order_price=stop_earning_order_price,
                                                         order_price_type='limit',
                                                         volume=ongoing_contract_count, ####
                                                         direction=stop_earning_direction,
                                                         offset='open',
                                                         lever_rate=10)

                # return False
            available_contract_count = max_contract_count - ongoing_contract_count
            if available_contract_count != max_contract_count:
                # 检查ongoing contract 是否有止盈止损，是否合理
                pass

            # 检查当前是否已经有挂单，挂单数量够不够
            if trend == 'long' and limit_to_buy_count > 0:
                pass

            # 设置limit挂单, 挂3档，把挂单数量分成3份
            first_position_available_contract_count = available_contract_count / 3
            second_position_available_contract_count = available_contract_count / 3
            third_position_available_contract_count = \
                max_contract_count - \
                (first_position_available_contract_count + second_position_available_contract_count)

            # 3档挂单以及每档挂单数量
            position_count = [first_position_available_contract_count, second_position_available_contract_count,
                              third_position_available_contract_count]

            for i in range(0, len(limit_price)):
                price = limit_price[i]
                volume = position_count[i]
                if volume > 0:
                    ret = dm.send_contract_order(symbol='BTC', contract_type='next_quarter', contract_code='',
                                                 client_order_id='', price=price, volume=volume,
                                                 direction=open_direction, offset='open', lever_rate=10,
                                                 order_price_type='limit')  # 已验证成功


            # 限价单操作
            '''
            ret = dm.send_contract_order(symbol='BTC', contract_type='next_quarter', contract_code='',
                                   client_order_id='', price=11886, volume=1, direction='sell',
                                   offset='open', lever_rate=10, order_price_type='limit')  # 已验证成功
            ret = dm.get_contract_open_orders("BTC")  # 已验证成功
            ret = dm.cancel_all_contract_order("BTC")  # 已验证成功
            ret = dm.get_contract_open_orders("BTC")  # 已验证成功
            '''
            # 委托单操作
            '''
            ret = dm.send_contract_trigger_order(symbol='BTC', contract_type='next_quarter', contract_code=None,
                                                 trigger_type='ge', trigger_price=11870, order_price=11880,
                                                 order_price_type='limit', volume=1, direction='sell', offset='open',
                                                 lever_rate=10)  # 已验证成功
            ret = dm.get_contract_trigger_openorders("BTC")  # 已验证成功
            ret = dm.cancel_all_contract_trigger("BTC")  # 已验证成功
            ret = dm.get_contract_trigger_openorders("BTC")  # 已验证成功
            '''
    """
    if 0:
        if last_ema_fast > last_ema_slow:
            print("long at {0}".format(last_ema_slow))

            # 1. 当前有单
            #    1.1 有空单 --> 平所有空单
            #    1.2 有多单
            #        1.2.1 有止盈止损 --> 忽略
            #        1.2.2 无止盈止损 --> 设置止盈止损(ema_slow + 200)
            # 2. 当前无单
            #     2.1 撤销之前所有挂单
            #     2.2 设置挂单 --> (ema_slow + 30, ema_slow - 20, ema_slow - 70)
            # 3.
        else:
            print("short at {0}".format(last_ema_slow))

        ma_table = Strategy1.Run(ma_fast, ma_slow, global_data)
        # SaveToFile(1, ma_table)
        macd, signal, hist = talib.MACD(np.array(close_list), fastperiod=12, slowperiod=26, signalperiod=9)
        global_data._hist_list = hist

        macd_state = 0
        for i in range(0, len(global_data._id_list)):
            ts = global_data._timestamp[i]
            macd = global_data._hist_list[i]
            # print("{0} - {1}".format(ts, macd))
            if macd_state == 0:
                if macd > 0:
                    macd_state = 1
                elif macd < 0:
                    macd_state = -1
            if (macd_state == 1 and macd < 0) or (macd_state == -1 and macd > 0):
                print("{0} - {1}".format(ts, macd))
                if macd > 0:
                    macd_state = 1
                elif macd < 0:
                    macd_state = -1
