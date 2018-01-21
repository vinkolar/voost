from inout.voiceinput import GoogleVoiceInput

class Input:
    def __init__(self, input_config):
        self._input = GoogleVoiceInput(input_config)
    
    def get_input(self):
        if(self._input):
            return self._input.get_voice_command()