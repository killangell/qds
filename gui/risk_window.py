from PyQt5 import QtWidgets, Qt
from gui.risk_gui import Ui_obj_risk


class RiskWindow(QtWidgets.QMainWindow, Ui_obj_risk):
    def __init__(self):
        super(RiskWindow, self).__init__()
        self.setupUi(self)
