# voost
This project helps to control Lego Boost on macOS using python3

# Getting started and installation
* [Install pygatt](https://github.com/peplin/pygatt). This helps us to communicate via bluetooth. We will slightly modify the source code to make it work on macOS
  ```bash
  pip3 install pygatt
  ```
* [Get pyb00st](https://github.com/JorgePe/pyb00st). This awesome library makes our life easier to manipulate lego motors and sensors. We will slightly modify the source code to make it work on macOS.
  ```bash
  git clone https://github.com/JorgePe/pyb00st.git
  ```
* [Install Bluetooth scanner]. This helps us to get the MAC address of our lego boost
  ```bash
  git clone https://github.com/jrowberg/bglib.git
  ```
* Install this project
  ```bash
  git clone https://github.com/vinkolar/voost.git
  ```

# Steps
* Get the Bluegiga (BLED112) USB dongle recognized on macOS [USB config] (./docs/installUSB.md)
* [Modify pyb00st to work on BLED112] (./docs/pyb00stChanges.md)
* Try examples

# Disclaimer:
LEGO and BOOST are Trademarks from The LEGO Company, which does not support this project. I am not responsible for any damage on your LEGO BOOST devices. (disclaimer copied and modified from pyb00st)