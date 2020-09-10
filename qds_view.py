import logging
import time
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTimer
from gui.qds_gui import Ui_qds_gui
from utils.singleton import mysington

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


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    ui = mywindow()
    ui.setWindowFlags(ui.windowFlags() & ~Qt.WindowMaximizeButtonHint)
    ui.setFixedSize(ui.width(), ui.height())
    ui.show()
    sys.exit(app.exec_())
