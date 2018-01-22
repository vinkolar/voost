from pyb00st.movehub import MoveHub
from pyb00st.constants import *
import sys

import logging
logger = logging.getLogger(__name__)

class Boost:
    def __init__(self, mac_addr, mode='Auto', hci="hci0"):
        self.mac_addr = mac_addr
        self.mode = mode
        self.hci = hci

    def init_hub(self):
        retval = {}
        self.my_movehub = MoveHub(self.mac_addr, self.mode, self.hci)
        try:
            self.my_movehub.start()
        except:
            err_msg = sys.exc_info()[0]
            logger.error("Could not INIT movehub({},{},{}). Error:{}".format(
                self.mac_addr, self.mode, self.hci, err_msg))
            retval['errStr'] = str(err_msg)
            self.try_stop_movehub()
        return retval

    def try_stop_movehub(self):
        if(self.my_movehub is not None):
            try:
                logger.error("Stopping movehub({},{},{})".format(
                    self.mac_addr, self.mode, self.hci))
                self.my_movehub.stop()
            except:
                err_msg = sys.exc_info()[0]
                logger.error("Could not STOP movehub({},{},{}). Error:{}".format(
                    self.mac_addr, self.mode, self.hci, err_msg))

    def try_move_hub(self, motor, time_ms, dutycycle_pct):
        retval = {}
        try:
            self.my_movehub.run_motor_for_time(motor, time_ms, dutycycle_pct)
        except:
            err_msg = sys.exc_info()[0]
            logger.error("Could not MOVE movehub({},{},{}). Error:{}".format(
                self.mac_addr, self.mode, self.hci, err_msg))
            #-- if(say_error):
            #--     say("Error while trying to move lego. {}".format(
            #--         sys.exc_info()[0]))
            retval['errStr'] = str(err_msg)
        return retval

    def go_forward_command(self):
        self.try_move_hub(MOTOR_AB, 2000, 100)

    def go_back_command(self):
        self.try_move_hub(MOTOR_AB, 2000, -100)
