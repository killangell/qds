class KLine:
    def __init__(self):
        self._amount = None
        self._ts = None
        self._ts_str = None
        self._open = None
        self._close = None
        self._high = None
        self._low = None
        self._vol = None

    def Equal(self, kline_other):
        if self._amount == kline_other._amount and \
                self._ts == kline_other._ts and \
                self._open == kline_other._open and \
                self._close == kline_other._close and \
                self._high == kline_other._high and \
                self._low == kline_other._low and \
                self._vol == kline_other._vol:
            return True
        else:
            return False
