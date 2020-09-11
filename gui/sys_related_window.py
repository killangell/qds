import sys
from PyQt5 import QtWidgets, Qt
from gui.sys_related import Ui_obj_sys_related


class SysRelatedWindow(QtWidgets.QMainWindow, Ui_obj_sys_related):
    def __init__(self):
        super(SysRelatedWindow, self).__init__()
        self.setupUi(self)

