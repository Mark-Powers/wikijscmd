import os
from configparser import ConfigParser

config_path = "/etc/wikijscmd/config.ini"
config = ConfigParser()
config.read(config_path)
