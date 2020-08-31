class Organized:
    def __init__(self):
        self._id_list = []
        self._timestamp = []
        self._close_list = []
        self._hist_list = []
        self._ma_list = [[0*1000]]*200
        self._ema_list = [[0*1000]]*200

    @property
    def ema_list(self):
        return self._ema_list

    def GetLen(self):
        return len(self._id_list)

    def GetId(self, index):
        return self._id_list[index]

    def GetTimestamp(self, index):
        return self._timestamp[index]

    def GetHist(self, index):
        return self._hist_list[index]

    def GetClose(self, index):
        return self._close_list[index]

    def GetEMA(self, period, index):
        return self._ema_list[period][index]