import threading
import time

from PyQt5 import QtWidgets
from qds_gui import Ui_qds_gui


class mywindow(QtWidgets.QMainWindow, Ui_qds_gui):
    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)


def listen_music(num):
    while True:
        print("----> %d" % num)
        print("begin to listen music at ", time.ctime())
        time.sleep(1)
        print("end to listen music at ", time.ctime())



if __name__ == "__main__":
    import sys
    """
    t1 = threading.Thread(target=listen_music, args=(13,))
    t1.start()
    """
    app = QtWidgets.QApplication(sys.argv)
    ui = mywindow()
    ui.show()
    sys.exit(app.exec_())
