import time

import goto
from openpyxl.chart import label

from data_source.huobi.HuobiDMService import HuobiDM

'''
URL = 'https://api.btcgateway.pro'

####  input your access_key and secret_key below:
ACCESS_KEY = '61bf2917-d263b13d-ghxertfvbf-1ebd5'
SECRET_KEY = '8eb611d4-7daf05ac-fc2c15ff-0b1ca'
udm = HuobiDM(URL, ACCESS_KEY, SECRET_KEY)
'''


class ParameterUtil:
    @staticmethod
    def get_reverse_diretion(direction):
        if direction == 'buy':
            return 'sell'
        elif direction == 'sell':
            return 'buy'
        else:
            return None


class ReturnUtil:
    @staticmethod
    def get_status(return_val):
        return return_val['status']

    @staticmethod
    def is_ok(return_val):
        return ReturnUtil.get_status(return_val) == 'ok'

    @staticmethod
    def get_ts(return_val):
        return return_val['ts']

    @staticmethod
    def get_data_all(return_val):
        return return_val['data']

    @staticmethod
    def get_data_list_size(return_val):
        return len(ReturnUtil.get_data_all(return_val))

    @staticmethod
    def get_data_item(index, return_val):
        return ReturnUtil.get_data_all(return_val)[index]

    @staticmethod
    def get_data_item_field(index, field, return_val):
        return ReturnUtil.get_data_item(index, return_val)[field]

    # 根据持仓方向（buy/sell）获取持仓数量
    @staticmethod
    def get_contract_position_count_by_direction(direction, return_val):
        count = 0
        for i in range(0, ReturnUtil.get_data_list_size(return_val)):
            dirt = ReturnUtil.get_data_item_field(i, 'direction', return_val)
            if dirt == direction:
                count += 1
        return count

class ReliableHuobiDM(HuobiDM):

    # 闪电平仓
    def reliable_send_lightning_close_position(self, symbol, contract_type, contract_code,
                                               volume, direction, client_order_id, order_price_type):
        ret = super().send_lightning_close_position(symbol, contract_type, contract_code, volume,
                                                    direction, client_order_id, order_price_type)
        if ReturnUtil.is_ok(ret):
            return True

        try_count = 0
        max_count = 3
        while True:
            if try_count >= max_count:
                return False

            tmp_ret = super().get_contract_position_info(symbol)
            if ReturnUtil.is_ok(tmp_ret):
                size = ReturnUtil.get_data_list_size(tmp_ret)
                if size == 0:
                    return True

                for i in range(0, size):
                    dirt = ReturnUtil.get_data_item_field(i, 'direction', tmp_ret)
                    if dirt == ParameterUtil.get_reverse_diretion(direction):
                        try_count += 1
                        ret = super().send_lightning_close_position(symbol, contract_type, contract_code, volume,
                                                                    direction, client_order_id, order_price_type)
                        if ReturnUtil.is_ok(ret):
                            return True
            else:
                try_count += 1
                time.sleep(3)