from xml.dom.minidom import parse


class ConfigData:
    def __init__(self):
        # account
        self._access_key = None
        self._secret_key = None
        # params
        self._period = None
        self._level_rate = None
        self._ma_fast = None
        self._ma_slow = None
        self._open_offset = None
        self._stop_offset = None
        self._max_open_number = None


class ConfigHelper:
    def __init__(self, file=None):
        self.file = file
        self.root = None

    def init_root(self):
        try:
            dom = parse(self.file)
            self.root = dom.documentElement
            return True
        except Exception as e:
            return False

    def get_node_value(self, name=None):
        node_list = self.root.getElementsByTagName(name)
        if (len(node_list)) == 0:
            return None
        value = node_list[0].childNodes[0].nodeValue
        return value

    def parse(self, config=ConfigData()):
        config._access_key = self.get_node_value('access_key')
        config._secret_key = self.get_node_value('secret_key')
        config._period = self.get_node_value('period')
        config._ma_fast = self.get_node_value('ema_fast')
        config._ma_slow = self.get_node_value('ema_slow')
        config._open_offset = self.get_node_value('one_time_open')
        # config._multi_times_open = self.get_node_value('multi_times_open')
        # config._stop_earning_offset = self.get_node_value('stop_earning_offset')
        # config._stop_loss_offset = self.get_node_value('stop_loss_offset')
        config._stop_offset = self.get_node_value('stop_earning_offset')
        config._level_rate = self.get_node_value('level_rate')
        config._max_open_number = self.get_node_value('max_open_number')


if __name__ == "__main__":
    file = 'config.xml'
    config_helper = ConfigHelper(file)
    config = ConfigData()
    ret = config_helper.init_root()
    if ret:
        config_helper.parse(config)
        a = config._access_key
        b = config._secret_key
        c = config._period
        d = config._ma_fast
        e = config._ma_slow
        f = config._open_offset
        g = config._stop_offset
        h = config._level_rate
        i = config._max_open_number
        j = 0
    else:
        print("error file {0}".format(file))
