import speech_recognition as sr
import subprocess
import time
import sys
from pyb00st.movehub import MoveHub
from pyb00st.constants import *

MY_MOVEHUB_ADD = '00:16:53:A8:0B:B0'
MY_MOVEHUB_MODE = 'Auto'
MY_BTCTRLR_HCI = 'hci0'
GO_FORWARD_STR = "go forward"
GO_BACK_STR = "go back"
TURN_RIGHT_STR = "turn right"
TURN_LEFT_STR = "turn left"
STOP_LEGO_STR = "stop lego"

def say(text_to_say):
    subprocess.call(['say', text_to_say])

def get_voice_command():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    text_said = None
    # Speech recognition using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        text_said = r.recognize_google(audio)
        print("You said: " + text_said )
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        say("Oops. Error during recognizing speech: Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        say("Oops. Error during recognizing speech. Could not request results from Google Speech Recognition service. Error {0}".format(e))
    
    return text_said

def try_stop_movehub(my_movehub):
    if(my_movehub is not None):
        try:
            my_movehub.stop()
        except:
            pass

def init_lego():
    retval = {}
    my_movehub = MoveHub(MY_MOVEHUB_ADD, MY_MOVEHUB_MODE, MY_BTCTRLR_HCI)
    retval['movehub'] = my_movehub
    try:
        my_movehub.start()
    except:
        retval['errStr'] =  str(sys.exc_info()[0])
        retval['movehub'] =  None
        try_stop_movehub(my_movehub)
        
    return retval

def try_move_hub(my_movehub, motor, time_ms, dutycycle_pct, say_error = False):
    retval = {}
    try:
        my_movehub.run_motor_for_time(motor, time_ms, dutycycle_pct)
    except:
        print("Error: {}".format(sys.exc_info()[0]))
        if(say_error):
            say("Error while trying to move lego. {}".format(sys.exc_info()[0]))
        retval['errStr'] = str(sys.exc_info()[0]) 
    return retval


def get_user_name():
    say("Hi, This is Voost. Today we will do something interesting. What is your name?")
    user_name = get_voice_command()
    
    while(True):
        if user_name is None:
           say("Oh..Sorry I couldnt get your name. Can you please tell me your name?")
        elif len(user_name) > 50:
            say("Oh..Thats a long name. Can you please tell me a short name that I can call you?")
        else:
            break

    say("Hi {}. Nice to meet you. Today, I will try to do the things that you say.".format(user_name))
    return user_name

def say_dint_understand(text_said):
    say("Hmm... Please tell me instructions that I can understand. I dont understand the instruction you said. {}".format(text_said))

def say_instructions():
    say("I can act on the following commands")
    time.sleep(0.5)
    say("First command is {}".format(GO_FORWARD_STR))
    time.sleep(0.5)
    say("Second command is {}".format(GO_BACK_STR))
    time.sleep(0.5)
    say("Third command is {}".format(STOP_LEGO_STR))

def go_forward_command(my_movehub):
    try_move_hub(my_movehub, MOTOR_AB, 2000, 100, say_error=True)

def go_back_command(my_movehub):
    try_move_hub(my_movehub, MOTOR_AB, 2000, -100, say_error=True)

def process_voice_command(text_said, my_movehub, user_name):
    retval = -2
    if(text_said is not None):
        if(text_said.lower().startswith(GO_FORWARD_STR.lower())):
            go_forward_command(my_movehub)
            retval = 0
        elif(text_said.lower().startswith(GO_BACK_STR.lower())):
            go_back_command(my_movehub)
            retval = 0
        elif(text_said.lower().startswith(STOP_LEGO_STR.lower())):
            say("Stopping Lego")
            try_stop_movehub(my_movehub)
            say("Stoped Lego. Good bye {}".format(user_name))
            retval = -1
        else:
            say("Sorry did not understand the command. Please try again")
            retval = 0
    return retval

def listen_to_voice_and_act(my_movehub, user_name):
    while(True):
        say("Hey {}. Tell me what to do".format(user_name))
        text_said = get_voice_command()
        ret = process_voice_command(text_said, my_movehub, user_name)
        if(ret < 0):
            break
        time.sleep(5)

def main(args):
    say("Will initialize lego boost. Please turn on lego")
    init_status = init_lego()
    if(init_status is None):
        say("Unable to start Lego Boost. Unknown Error")
        return -1
    elif(init_status.get('errStr', None) is not None):
        say("Unable to start Lego Boost. Unknown Error")
        return -1
    my_movehub = init_status.get('movehub', None)
    if(my_movehub is None):
        say("Unable to start Lego Boost. Move hub is null") 
        return -1
    say("All initialized.")
    
    time.sleep(1)
    user_name = get_user_name()
    if(user_name is not None):
        say_instructions()
    
    listen_to_voice_and_act(my_movehub, user_name)

if __name__ == "__main__":
    main(None)