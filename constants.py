import os
from configparser import RawConfigParser

config = RawConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "CONF.ini"))

FB_LOGIN = config.get("login_settings", "FB_LOGIN")
FB_PASSWORD = config.get("login_settings", "FB_PASSWORD")
SLEEP_TIME = config.get("general_settings", "SLEEP_TIME")
MESSAGE_ON_SEND = config.get("general_settings", "MESSAGE_ON_SEND")
