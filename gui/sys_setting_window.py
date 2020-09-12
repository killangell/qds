from PyQt5 import QtWidgets, Qt
from gui.sys_setting_gui import Ui_obj_sys_setting


class SysSettingWindow(QtWidgets.QMainWindow, Ui_obj_sys_setting):
    def __init__(self):
        super(SysSettingWindow, self).__init__()
        self.setupUi(self)

