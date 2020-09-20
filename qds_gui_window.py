import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

from gui.qds_gui import Ui_qds_gui
from utils.singleton import Singleton

instance = Singleton()


class QdsWindow(QtWidgets.QMainWindow, Ui_qds_gui):
    def __init__(self):
        super(QdsWindow, self).__init__()
        ret = instance.detect_instance()
        if not ret:
            QMessageBox.information(self, '提示', '同一目录，只允许一个实例运行')
            sys.exit(-1)

        self.setupUi(self)

    def closeEvent(self, event):  # 函数名固定不可变
        instance.delete_lok_file()

    """
    def closeEvent(self, event):#函数名固定不可变
        reply=QtWidgets.QMessageBox.question(self,u'警告',u'确认退出?',QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
        #QtWidgets.QMessageBox.question(self,u'弹窗名',u'弹窗内容',选项1,选项2)
        if reply==QtWidgets.QMessageBox.Yes:
            event.accept()#关闭窗口
        else:
            event.ignore()#忽视点击X事件
    """