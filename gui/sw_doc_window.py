from PyQt5 import QtWidgets, Qt
from gui.sw_doc_gui import Ui_obj_sw_doc


class SWDOCWindow(QtWidgets.QMainWindow, Ui_obj_sw_doc):
    def __init__(self):
        super(SWDOCWindow, self).__init__()
        self.setupUi(self)
