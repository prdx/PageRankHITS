import yaml

class Config(object):
    __config = {}

    @staticmethod
    def get(name):
        if name in Config.__config:
            return Config.__config[name]
        else:
            return ""

    def __init__(self, config_path):
        try:
            with open(config_path, 'r') as config:
                config_str = config.read()
                Config.__config = yaml.load(config_str)

        except Exception as exception:
            raise exception

