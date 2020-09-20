from xml.dom.minidom import parse


class ConfigData:
    def __init__(self):
        self.root = None
        self.dom = None
        # account
        self._access_key = None
        self._secret_key = None
        # params
        self._period = None
        self._level_rate = None
        self._ema_fast = None
        self._ema_slow = None
        self._open_offset = None
        self._open_interval = None
        self._stop_earning_offset = None
        self._max_open_number = None
        self._max_open_number_limit = None
        self._qds_id = None


class ConfigHelper:
    def __init__(self, file=None):
        self.file = file
        self.root = None

    def init_root(self):
        try:
            self.dom = parse(self.file)
            self.root = self.dom.documentElement
            return True
        except Exception as e:
            return False

    def get_node_value(self, name=None):
        node_list = self.root.getElementsByTagName(name)
        if (len(node_list)) == 0:
            return None
        value = node_list[0].childNodes[0].nodeValue
        return value

    def set_node_value(self, name=None, value=None):
        node_list = self.root.getElementsByTagName(name)
        if (len(node_list)) == 0:
            return False
        node_list[0].childNodes[0].data = value
        return True

    def parse(self, config=ConfigData()):
        config._access_key = self.get_node_value('access_key')
        config._secret_key = self.get_node_value('secret_key')
        config._period = self.get_node_value('period')
        config._ema_fast = self.get_node_value('ema_fast')
        config._ema_slow = self.get_node_value('ema_slow')
        config._open_offset = self.get_node_value('open_offset')
        config._open_interval = self.get_node_value('open_interval')
        config._stop_earning_offset = self.get_node_value('stop_earning_offset')
        config._level_rate = self.get_node_value('level_rate')
        config._max_open_number = self.get_node_value('max_open_number')
        config._max_open_number_limit = self.get_node_value('max_open_number_limit')
        config._qds_id = self.get_node_value('qds_id')

    def save(self, config=ConfigData()):
        self.set_node_value('access_key', config._access_key)
        self.set_node_value('secret_key', config._secret_key)
        self.set_node_value('period', config._period)
        self.set_node_value('ema_fast', config._ema_fast)
        self.set_node_value('ema_slow', config._ema_slow)
        self.set_node_value('open_offset', config._open_offset)
        self.set_node_value('open_interval', config._open_interval)
        self.set_node_value('stop_earning_offset', config._stop_earning_offset)
        self.set_node_value('level_rate', config._level_rate)
        self.set_node_value('max_open_number', config._max_open_number)
        if config._max_open_number_limit:
            self.set_node_value('max_open_number_limit', config._max_open_number_limit)
        self.set_node_value('qds_id', config._qds_id)
        with open(self.file, "w", encoding="utf-8") as f:
            self.dom.writexml(f)


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
        d = config._ema_fast
        e = config._ema_slow
        f = config._open_offset
        g = config._open_interval
        h = config._stop_earning_offset
        i = config._level_rate
        j = config._max_open_number
        k = config._max_open_number_limit
        l = config._qds_id
        m = 0

        config_to_save = ConfigData()
        config_to_save._access_key = '_access_key'
        config_to_save._secret_key = '_secret_key'
        config_to_save._period = '_period'
        config_to_save._ema_fast = '_ema_fast'
        config_to_save._ema_slow = '_ema_slow'
        config_to_save._open_offset = '_open_offset'
        config_to_save._open_interval = '_open_interval'
        config_to_save._stop_earning_offset = '_stop_earning_offset'
        config_to_save._level_rate = '_level_rate'
        config_to_save._max_open_number = 'max_open_number'
        config_to_save._max_open_number_limit = 'max_open_number_limit'
        config_to_save._qds_id = 'qds_id'
        config_helper.save(config_to_save)
    else:
        print("error file {0}".format(file))
