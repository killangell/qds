import time
import json
from model.kline import KLine
from data_source.kline_adapter_base import KLineAdapterBase
from model.organized import Organized

from data_source.huobi.static_data_source.huobi_15min_data_source import Huobi15minData


class KLineAdapterHuobi(KLineAdapterBase):

    @staticmethod
    def ConvertTimeStamp(ts):
        currentTimeStamp = int(ts)
        time_local = time.localtime(currentTimeStamp)  # 格式化时间戳为本地时间
        time_YmdHMS = time.strftime("%Y%m%d_%H%M%S", time_local)  # 自定义时间格式
        # print('currentTimeStamp:', currentTimeStamp)
        # print('time_local:', time_local)
        # print('time_YmdHMS:', time_YmdHMS)
        return time_YmdHMS

    def ConvertSingleData(self, source_data):
        data = KLine()
        data._amount = source_data["amount"]
        data._ts = source_data["id"]
        data._ts_str = KLineAdapterHuobi.ConvertTimeStamp(source_data["id"])
        data._open = source_data["open"]
        data._close = source_data["close"]
        data._high = source_data["high"]
        data._low = source_data["low"]
        data._vol = source_data["vol"]
        return data

    def GetKLineDataList(self, period, size):
        data_source = Huobi15minData.GetTestData_15min_1000
        kline_data_dict = data_source()
        kline_data_str = json.dumps(kline_data_dict)
        jsl = json.loads(kline_data_str)
        return self.ConvertListData(jsl["data"])

    def GetClose(self, source_data):
        return source_data["close"]

    def GetCloseList(self, source_kline_list):
        pass

    @staticmethod
    def ParseData(source_kline_list):
        org = Organized()
        source_kline_list.sort(key=lambda x: x['id'])
        for kline in source_kline_list:
            org._id_list.append(kline['id'])
            org._timestamp.append(KLineAdapterHuobi.ConvertTimeStamp(kline['id']))
            org._close_list.append(kline['close'])
        return org
