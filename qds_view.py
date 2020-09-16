import logging
import time
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from qds_gui_window import QdsWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = QdsWindow()
    ui.setWindowFlags(ui.windowFlags() & ~Qt.WindowMaximizeButtonHint)
    ui.setFixedSize(ui.width(), ui.height())
    ui.show()
    sys.exit(app.exec_())
