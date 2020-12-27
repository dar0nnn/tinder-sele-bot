import logging.config
import os

from tinder import Tinder

logging.config.fileConfig(
    fname=os.path.join(os.path.dirname(__file__), 'LOGGER_CONFIG.ini'),
    disable_existing_loggers=False,
)
tinder = Tinder()
tinder.login()

while True:
    choice = 'like'
    tinder.command(choice)
