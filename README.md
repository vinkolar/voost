# voost
Voost project creates a Voice activated Lego boost using bluetooth connectivity and [Google Speech API](https://cloud.google.com/speech/) (and [Speech Recognition](https://pypi.python.org/pypi/SpeechRecognition/)). 

The main goal is to first have a conversational interface where humans can talk to lego. Currently we are far from it. Voost currently acts on the following simple commands using voice input:
* Go forward
* Go back
* Stop lego

In addition, it also has some voice interface to prompt for user's name, and sort of other miscellaneous things.

Limitations: 
* Voost now works only on Lego Boost on macOS using python3
* Need to buy a bluetooth BLED device to communicate

Try it and let me know how it works.

# Getting started and installation
* [Install pygatt](https://github.com/peplin/pygatt). This helps us to communicate via bluetooth. We will slightly modify the source code to make it work on macOS
  ```bash
  pip3 install pygatt
  ```
* [Get pyb00st](https://github.com/JorgePe/pyb00st). This awesome library makes our life easier to manipulate lego motors and sensors. We will slightly modify the source code to make it work on macOS. Go to the directory where you want to clone ```pyb00st```, and use the below command for cloning.
  ```bash
  git clone https://github.com/JorgePe/pyb00st.git
  ```
* [Install Bluetooth scanner]. This helps us to get the MAC address of our lego boost. Go to the directory where you want to clone ```bglib```, and use the below command for cloning.
  ```bash
  git clone https://github.com/jrowberg/bglib.git
  ```
* Install Audio recognition: This is going to be enabled by installing pyaudio, speech recognition (tied with Google Voice APIs)
  * Install LLVM with clang and ```portaudio```. We need this for other packages to be installed
    ```bash
    brew install --with-clang llvm
    brew install portaudio
    ```
  * Install pyaudio
    ```bash
    pip3 install pyaudio
    ```
  * Install [SpeechRecognition](https://pypi.python.org/pypi/SpeechRecognition/)
    ```bash
    pip3 install SpeechRecognition
    ```
* Install this project.  Go to the directory where you want to clone ```voost```, and use the below command for cloning.
  ```bash
  git clone https://github.com/vinkolar/voost.git
  ```

# Steps
* Get the Bluegiga (BLED112) USB dongle recognized on macOS [USB config](./docs/installUSB.md)
* [Get the MAC address of Lego Boost](./docs/macAddress.md) so that we can communicate with it
* You can now try all examples in the ```examples``` (in ```pyb00st``` project folder, and not in this projects folder). In all the pyb00st example files, please change the below:
  * Change MAC address to your Lego boost's MAC address. This can be got from [scanning](./docs/macAddress.md). This MAC address is the first argument in ```Movehub(...)``` constructor.
  * Change the mode to reflect BLED112 dongle mode (```Auto``` and not ```BlueZ``` as in pyb00st defautl arguments). This is the second argument in ```Movehub(...)``` constructor
  * Example changes in ```https://github.com/JorgePe/pyb00st/blob/master/examples/color_controlled_car.py```:
    ```python
    ...
    MY_MOVEHUB_ADD = '00:16:53:A8:0B:B0'
    MY_BTCTRLR_HCI = 'hci0'

    mymovehub = MoveHub(MY_MOVEHUB_ADD, 'Auto', MY_BTCTRLR_HCI)
    mymovehub.subscribe_all()
    ...
    ```
* There is just one more glitch you may experience when running pyb00st examples. ```pyb00st``` assumes that you use ```gatttool```. Note that on macOS, we use BGAPI adapter instead of GATT (we are using BGAPI backend instead of GATTTool backend). Currently please use [this temporary fix](https://github.com/JorgePe/pyb00st/issues/7) in ```pyb00st```
* Try all examples from pyb00st
* Now, try the voice activated lego boost using the coommand below:
```bash
Vinays-MacBook:voost vinkolar$ python3 test/voice_actions.py
```

Let me know if you face any problem in enabling python over Lego boost on macOS

# Disclaimer:
LEGO and BOOST are Trademarks from The LEGO Company, which does not support this project. I am not responsible for any damage on your LEGO BOOST devices. (disclaimer copied and modified from pyb00st)