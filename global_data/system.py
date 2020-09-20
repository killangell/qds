g_system_running = False
g_margin_available, g_margin_balance = 0.0, 0.0


def set_system_running(en):
    global g_system_running
    g_system_running = en


def get_system_running():
    global g_system_running
    return g_system_running


def set_margin(available, balance):
    global g_margin_available, g_margin_balance
    g_margin_available, g_margin_balance = available, balance


def get_margin():
    global g_margin_available, g_margin_balance
    return g_margin_available, g_margin_balance
