from PyQt5 import QtWidgets
from gui.qds_gui import Ui_qds_gui


class QdsWindow(QtWidgets.QMainWindow, Ui_qds_gui):
    def __init__(self):
        super(QdsWindow, self).__init__()
        self.setupUi(self)


