import sys
sys.path.insert(0,'./code')

import time
from inout import voiceinput, voiceoutput
from sensor import boost
from actors.user import User
from actors import robot

EXPERT_MODE = False
MY_MOVEHUB_ADD = '00:16:53:A8:0B:B0'
MY_MOVEHUB_MODE = 'Auto'
MY_BTCTRLR_HCI = 'hci0'

class VoostTalk:

    def __init__(self):
        self.out = voiceoutput.OsXVoiceOutput()
        self.inp = voiceinput.GoogleVoiceInput(self.out)
        self.voost = boost.Boost(MY_MOVEHUB_ADD, mode=MY_MOVEHUB_MODE, hci=MY_BTCTRLR_HCI)
        self.user = User(self.out, self.inp)
        self.boost_inited = self.init_boost()
        if(self.boost_inited):
            self.user_inited = self.init_user()
        else:
            self.user_inited = False

    def init_boost(self):
        self.out.output("Will initialize lego boost. Please turn on lego")
        init_status = self.voost.init_hub()
        if(init_status is None):
            self.out.output("Unable to start Lego Boost. Unknown Error")
            return False
        elif(init_status.get('errStr', None) is not None):
            self.out.output("Unable to start Lego Boost. Error: {}".format(init_status['errStr']))
            return False
        
        self.out.output("Voost device initialized.")
        return True

    def init_user(self):
        time.sleep(1)
        self.user.init(prompt=True)
        if(self.user.username is not None):
            self.output_instructions()
            self.listen_to_voice_and_act()
        return True

    def output_instructions(self):
        if(not EXPERT_MODE):
            self.out.output("I can act on the following commands")
            time.sleep(0.5)
            self.out.output("First command is {}".format(robot.GO_FORWARD_STR))
            time.sleep(0.5)
            self.out.output("Second command is {}".format(robot.GO_BACK_STR))
            time.sleep(0.5)
            self.out.output("Third command is {}".format(robot.STOP_LEGO_STR))

    def process_voice_command(self, text_said):
        retval = -2
        if(text_said is not None):
            if(text_said.lower().startswith(robot.GO_FORWARD_STR.lower())):
                self.voost.go_forward_command()
                retval = 0
            elif(text_said.lower().startswith(robot.GO_BACK_STR.lower())):
                self.voost.go_back_command()
                retval = 0
            elif(text_said.lower().startswith(robot.STOP_LEGO_STR.lower())):
                self.out.output("Stopping Lego")
                self.voost.try_stop_movehub()
                self.out.output("Stoped Lego. Good bye {}".format(self.user.username))
                retval = -1
            else:
                self.out.output("Sorry did not understand the command. Please try again")
                retval = 0
        return retval

    def listen_to_voice_and_act(self):
        while(True):
            self.out.output("Hey {}. Tell me what to do".format(self.user.username))
            text_said = self.inp.get_voice_command()
            ret = self.process_voice_command(text_said)
            if(ret < 0):
                break
            time.sleep(5)

def main(args):
    vtalk = VoostTalk()
    if(vtalk.boost_inited and vtalk.user_inited):
        vtalk.output_instructions()
        vtalk.listen_to_voice_and_act()

if __name__ == "__main__":
    main(None)