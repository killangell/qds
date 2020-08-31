class Cross:
    STATE_NONE = 0
    STATE_FAST_BELOW_SLOW = 1
    STATE_FAST_OVER_SLOW = 2

    @staticmethod
    def GetState(ma_fast, ma_slow, threshold):
        if ma_fast == ma_slow:
            return Cross.STATE_NONE, 0

        diff = abs(ma_fast - ma_slow)
        state = Cross.STATE_NONE
        if diff >= threshold:
            if ma_fast > ma_slow:
                state = Cross.STATE_FAST_OVER_SLOW
            else:
                state = Cross.STATE_FAST_BELOW_SLOW
            return state, diff
        else:
            return state, diff