import os
from configparser import ConfigParser

config_path = os.path.join(os.path.dirname(__file__), "config.ini")
config = ConfigParser()
config.read(config_path)
