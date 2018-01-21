from inout import output

class User:
    def __init__(self):
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

    def prompt_user_name(self):
        if self.username is not None:
            self.output("Hi, This is Voost. Today we will do something interesting. What is your name?")
            user_name = self.get_input()
            
            while(True):
                if user_name is None:
                    self.output("Oh..Sorry I couldnt get your name. Can you please tell me your name?")
                elif len(user_name) > 50:
                    self.output("Oh..Thats a long name. Can you please tell me a short name that I can call you?")
                else:
                    break

            self.output("Hi {}. Nice to meet you. Today, I will try to do the things that you say.".format(user_name))
            self.username = user_name
        return self.username

    def get_username(self, prompt_if_needed=False):
        if(self.username is None and prompt_if_needed):
            self.prompt_user_name()
        return self.username

    def init(self):
        self.get_username(prompt_if_needed=True)
        