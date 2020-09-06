import logging
import threading
import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTimer
from qds_gui import Ui_qds_gui
from qds import set_buniness_enabled, get_business_enabled

logging.basicConfig(level=logging.DEBUG,  # 控制台打印的日志级别
                    filename='qds.log',
                    filemode='w',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    # a是追加模式，默认如果不写的话，就是追加模式
                    format='%(asctime)s : %(message)s'
                    # '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    # 日志格式
                    )

class mywindow(QtWidgets.QMainWindow, Ui_qds_gui):
    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)
"""
        self.timer = QTimer(self)  # 初始化一个定时器
        self.timer.start(2000)  # 设置计时间隔并启动
        self.timer.timeout.connect(self.operate)  # 计时结束调用operate()方法

    def operate(self):
        enabled = get_business_enabled()
        if enabled:
            print('opened timer 60')
            time.sleep(10)
        else:
            print('closed timer')
"""
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
    ui.setWindowFlags(ui.windowFlags() & ~Qt.WindowMaximizeButtonHint)
    ui.show()
    sys.exit(app.exec_())
