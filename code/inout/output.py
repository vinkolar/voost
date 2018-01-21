import inout.voiceoutput

class Output:
    def __init__(self, output_config):
        self._output = voiceoutput.VoiceOutput(output_config)
    
    def output(self, text_to_output):
        if(self._output):
            return self._output.text_to_output()