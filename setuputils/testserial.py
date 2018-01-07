import pygatt
import logging
import time

logging.basicConfig()
logging.getLogger('pygatt').setLevel(logging.DEBUG)

import os
import termios
import serial


if(False):
    serial_port = '/dev/cu.usbmodem1'
    _ser = serial.Serial(serial_port, baudrate=115200,
                                          timeout=0.25)
                # Wait until we can actually read from the device
    _ser.read()
    #fd = os.open(dev, os.O_RDWR | os.O_NOCTTY | os.O_NONBLOCK)
    #print("fd:{}".format(fd))
    packet = b'\x00\x01\x00\x00\x00'
    
    for i in range(100):
        print("i={}".format(i))
        _ser.write(packet)
        time.sleep(5)
        _ser.flush()
        print("Written {}".format(i))
        
else:
    adapter = pygatt.BGAPIBackend()
    adapter.start()