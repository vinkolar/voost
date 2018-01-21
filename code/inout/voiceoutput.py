import subprocess

class OsXVoiceOutput:
    def output(self, text_to_say):
        subprocess.call(['say', text_to_say])