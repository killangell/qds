from model.kline import KLine


class KLineAdapterBase:
    def ConvertSingleData(self, source_data):
        print("KlineAdapterBase.ConvertSingleData called")
        pass

    def ConvertListData(self, source_data_list):
        kline_list = []
        for data in source_data_list:
            kline_data = self.ConvertSingleData(data)
            kline_list.append(kline_data)
        return kline_list

    def GetClose(self, source_data):
        print("KlineAdapterBase.GetClose called")
        pass

    def GetCloseList(self, source_data_list):
        close_list = []
        for data in source_data_list:
            close = self.GetClose(data)
            close_list.append(close)
        return close_list
