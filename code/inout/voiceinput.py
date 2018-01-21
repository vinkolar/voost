import speech_recognition as sr
import logging

logger = logging.getLogger(__name__)

class GoogleVoiceInput:
    def __init__(self):
        pass

    def set_output(self, output):
        self._output = output

    def output_text(self, text_to_out):
        if(self._output):
            self._output.output(text_to_out)

    def get_voice_command(self):
        # Record Audio
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.output_text("Say something!")
            audio = r.listen(source)
        text_said = None
        # Speech recognition using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            text_said = r.recognize_google(audio)
            self.output_text("You said: " + text_said)
        except sr.UnknownValueError:
            logger.error(
                "Google Speech Recognition could not understand audio")
            self.output_text(
                "Oops. Error during recognizing speech: Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            logger.error(
                "Could not request results from Google Speech Recognition service; {0}".format(e))
            self.output_text(
                "Oops. Error during recognizing speech. Could not request results from Google Speech Recognition service. Error {0}".format(e))

        return text_said
