import math

from model.ma_table import MaTable
from model.organized import Organized
from control.ma.cross import Cross


class Strategy1:
    @staticmethod
    def Run(period_fast, period_slow, org: Organized, verbose=False):
        length = len(org._id_list)
        threshold = 0
        price_init = 0.0
        profit_sum = 0.0
        profit_onetime = 0.0
        # stats counter
        negative_number = 0
        positive_number = 0
        win = False
        rate = 0.0

        for start_index in range(0, length):
            ma_fast = org.GetEMA(period_fast, start_index)
            ma_slow = org.GetEMA(period_slow, start_index)
            close = org.GetClose(start_index)
            timestamp = org.GetTimestamp(start_index)
            if math.isnan(ma_fast) or math.isnan(ma_slow):
                continue
            state_init, diff = Cross.GetState(ma_fast, ma_slow, threshold)
            break

        for index in range(start_index + 1, length):
            ma_fast = org.GetEMA(period_fast, index)
            ma_slow = org.GetEMA(period_slow, index)
            close = org.GetClose(index)
            timestamp = org.GetTimestamp(index)
            price_cur = close
            # if verbose:
            #    print("index:{0} slow={1} fast={2} close={3}, timestamp={4}".format(index, ma_slow, ma_fast, close, timestamp))

            state_cur, diff = Cross.GetState(ma_fast, ma_slow, threshold)
            if state_init != state_cur:
                if (state_init == Cross.STATE_NONE and state_cur == Cross.STATE_FAST_OVER_SLOW) or (
                        state_init == Cross.STATE_FAST_BELOW_SLOW and state_cur == Cross.STATE_FAST_OVER_SLOW):
                    if price_init:
                        profit_onetime = price_init - price_cur
                        profit_sum += profit_onetime
                        if profit_onetime > 0:
                            positive_number += 1
                        else:
                            negative_number += 1
                        if verbose:
                            print("{0}: long, {1} - *{2} = {3}, sum:{4}, diff:{5}".format(timestamp, price_init, price_cur,
                                                                                      profit_onetime, profit_sum, diff))
                    else:
                        price_init = close
                        if verbose:
                            print("{0}: long, close:{1}, diff{2}".format(timestamp, close, diff))
                else:
                    if price_init:
                        profit_onetime = price_cur - price_init
                        profit_sum += profit_onetime
                        if profit_onetime > 0:
                            positive_number += 1
                        else:
                            negative_number += 1
                        if verbose:
                            print("{0}: short, *{1} - {2} = {3}, sum:{4}, diff:{5}".format(timestamp, price_cur, price_init,
                                                                                       profit_onetime, profit_sum,
                                                                                       diff))
                    else:
                        price_init = close
                        if verbose:
                            print("{0}: short, close: {1}, diff:{2}".format(timestamp, close, diff))
                state_init = state_cur

        total_number = positive_number + negative_number
        rate = round((positive_number * 100) / total_number, 2)
        win = positive_number > negative_number
        return MaTable(period_fast, period_slow, threshold, profit_sum, total_number,
                       positive_number, negative_number, win, rate)
