import sys
import urllib3

from utilities.config import Config

class Base(object):
    _config = None

    def __init__(self, path: str = "config.yaml"):
        urllib3.disable_warnings()
        self._config = Config.get_instance(path)