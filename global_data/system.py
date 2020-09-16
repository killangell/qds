from PyQt5 import QtWidgets
# from qds_gui_window import QdsWindow

g_system_running = False
g_margin = 0.0
g_qds_gui_window = None # QdsWindow()


def set_system_running(en):
    global g_system_running
    g_system_running = en


def get_system_running():
    global g_system_running
    return g_system_running


def set_margin(margen):
    global g_margin
    g_margin = margen


def get_margin():
    global g_margin
    return g_margin


def get_qds_gui_window():
    global g_qds_gui_window
    return g_qds_gui_window

