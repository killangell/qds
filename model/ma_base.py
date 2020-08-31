import logging


class MABase:
    _MA_STATE_EQUAL = 1
    _MA_ELEM_MAX = 180
    _MA_INIT = -1

    def __init__(self):
        self._ma_list = [MABase._MA_INIT] * MABase._MA_ELEM_MAX

    def GetMAList(self):
        return self._ma_list

    def SetMA(self, period, ma):
        if not MABase.ValidPeiod(period):
            print("SetMA： Invalid input: period={0}, ma={1}".format(period, ma))
            assert False
        self._ma_list[period - 1] = ma

    def GetMA(self, period):
        if not MABase.ValidPeiod(period):
            print("GetMA： Invalid input: period={0}".format(period))
            assert False
        return self._ma_list[period - 1]

    def Equal(self, ma_elem_other):
        if self._ma_list == ma_elem_other.GetMAList():
            return True
        else:
            return False

    @staticmethod
    def ValidPeiod(period):
        if 0 < period <= MABase._MA_ELEM_MAX:
            return True
        else:
            return False

    def Print(self):
        logging.debug("MAElem: ")
        index = 0
        for ma in self._ma_list:
            if ma != -1:
                logging.debug("{0}:{1} ".format(index + 1, ma))
            index += 1
        logging.debug("")

    @property
    def MA_INIT(self):
        return self._MA_INIT

    @property
    def MA_STATE_EQUAL(self):
        return self._MA_STATE_EQUAL