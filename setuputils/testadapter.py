import pygatt
import logging
import time

logging.basicConfig()
logging.getLogger('pygatt').setLevel(logging.DEBUG)

import os
import termios
import serial

adapter = pygatt.BGAPIBackend()
adapter.start()