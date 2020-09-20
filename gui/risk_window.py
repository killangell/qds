import sys

from PyQt5 import QtWidgets, Qt
from gui.risk_gui import Ui_obj_risk


class RiskWindow(QtWidgets.QMainWindow, Ui_obj_risk):
    def __init__(self):
        super(RiskWindow, self).__init__()
        self.setupUi(self)

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, u'警告', u'同意并继续?',
                                               QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            sys.exit(-1)