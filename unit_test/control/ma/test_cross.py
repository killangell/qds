from control.ma.cross import Cross


class TestCross:
    @staticmethod
    def TestGetSate():
        test_data = [
            #   [fast, slow, threshold, (state, diff)]
            [0, 0, 0, (Cross.STATE_NONE, 0)],
            [0, 1, 0, (Cross.STATE_FAST_BELOW_SLOW, 1)],
            [1, 0, 0, (Cross.STATE_FAST_OVER_SLOW, 1)],
            [10, 30, 0, (Cross.STATE_FAST_BELOW_SLOW, 20)],
            [30, 10, 0, (Cross.STATE_FAST_OVER_SLOW, 20)],
            [0, 0, 10, (Cross.STATE_NONE, 0)],
            [0, 1, 10, (Cross.STATE_NONE, 1)],
            [1, 0, 10, (Cross.STATE_NONE, 1)],
            [10, 30, 10, (Cross.STATE_FAST_BELOW_SLOW, 20)],
            [30, 10, 10, (Cross.STATE_FAST_OVER_SLOW, 20)]
        ]
        print("test cross: test started")

        for index in range(0, len(test_data)):
            fast = test_data[index][0]
            slow = test_data[index][1]
            threshold = test_data[index][2]
            expect = test_data[index][3]
            result = Cross.GetState(fast, slow, threshold)
            assert (expect == result)
            print("test cross: index = {0}".format(index))

        print("test cross: test passed")


if __name__ == "__main__":
    TestCross.TestGetSate()