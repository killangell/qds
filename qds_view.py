import logging
import time
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
# from global_data.system import get_qds_gui_window
from gui.qds_gui import Ui_qds_gui
from qds_gui_window import QdsWindow


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = QdsWindow() # get_qds_gui_window() # qds_gui_window()
    ui.setWindowFlags(ui.windowFlags() & ~Qt.WindowMaximizeButtonHint)
    ui.setFixedSize(ui.width(), ui.height())
    ui.show()
    sys.exit(app.exec_())
