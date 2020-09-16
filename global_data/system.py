g_system_running = False
g_margin = 0.0


def set_system_running(en):
    global g_system_running
    g_system_running = en


def get_system_running():
    global g_system_running
    return g_system_running


def set_margin(margin):
    global g_margin
    g_margin = margin


def get_margin():
    global g_margin
    return g_margin
