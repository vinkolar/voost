from inout import input, output
import time
from sensor import boost

GO_FORWARD_STR = "go forward"
GO_BACK_STR = "go back"
TURN_RIGHT_STR = "turn right"
TURN_LEFT_STR = "turn left"
STOP_LEGO_STR = "stop lego"

class Robot:
    def __init__(self, boost):
        self.boost = boost
        pass

    def set_output(self, output):
        self._output = output

    def set_input(self, input_obj):
        self._input = input_obj

    def output(self, text_to_out):
        if(self._output):
            self._output.output(text_to_out)

    def get_input(self):
        if(self._input):
            return self._input.get_input()

    def say_dint_understand(self, text_said):
        self.output(
            "Hmm... Please tell me instructions that I can understand. I dont understand the instruction you said. {}".format(text_said))

    def say_instructions(self):
        self.output("I can act on the following commands")
        time.sleep(0.5)
        self.output("First command is {}".format(GO_FORWARD_STR))
        time.sleep(0.5)
        self.output("Second command is {}".format(GO_BACK_STR))
        time.sleep(0.5)
        self.output("Third command is {}".format(STOP_LEGO_STR))

    def process_voice_command(self, text_said, my_movehub, user_name):
        retval = -2
        if(text_said is not None):
            if(text_said.lower().startswith(GO_FORWARD_STR.lower())):
                boostcommands.go_forward_command(my_movehub)
                retval = 0
            elif(text_said.lower().startswith(GO_BACK_STR.lower())):
                boostcommands.go_back_command(my_movehub)
                retval = 0
            elif(text_said.lower().startswith(STOP_LEGO_STR.lower())):
                self.output("Stopping Lego")
                boostcommands.try_stop_movehub(my_movehub)
                self.output("Stoped Lego. Good bye {}".format(user_name))
                retval = -1
            else:
                self.output(
                    "Sorry did not understand the command. Please try again")
                retval = 0
        return retval

    def listen_to_voice_and_act(self, my_movehub, user_name):
        while(True):
            self.output("Hey {}. Tell me what to do".format(user_name))
            text_said = self.get_input()
            ret = self.process_voice_command(text_said, my_movehub, user_name)
            if(ret < 0):
                break
            time.sleep(5)
