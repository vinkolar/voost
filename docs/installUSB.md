# Configuring BLED112 dongle
* Buy the BLED112 dongle [Bluegiga USB Dongle](https://www.amazon.com/gp/product/B00HKILG1W). Its around $18 incl. shipping (in US)
* Plug it into the Mac book (my mac book: MacOS High Sierra, version 10.13.2)
* Make sure the device is detected
  * Go to `Apple Icon` -> `About this Mac`
  * Click on `System Report` button in the `Overview` tab 

    <img src="./images/sysOverview.png" alt="sysOverview" style="width: 200px;"/>
  * In the left pane go to `Hardware` -> `USB`

    <img src="./images/lowEnergyDongle.png" alt="bled112" style="width: 400px;"/>
  * On the right pane `USB Device Tree`, click on `Low Energy Dongle` (see above pic)
  * Make sure that of the following (else it wont work with current version of pyb00st)
    * `Product ID:	0x0001`
    * `Vendor ID:	0x2458`

* Test the `pygatt` adapter by running the [testadapter.py](./setuputils/testadapter.py)
  ```bash
  Vinays-MacBook:voost vinkolar$ python3 setuputils/testadapter.py
  INFO:pygatt.backends.bgapi.bgapi:Initialized new BGAPI backend
  DEBUG:pygatt.backends.bgapi.bgapi:Opening connection to serial port (attempt 1)
  INFO:pygatt.backends.bgapi.bgapi:Auto-detecting serial port for BLED112
  DEBUG:pygatt.backends.bgapi.util:Found 3 serial USB devices
  DEBUG:pygatt.backends.bgapi.util:Checking serial USB device: /dev/cu.SSDC - n/a
  DEBUG:pygatt.backends.bgapi.util:Checking serial USB device: /dev/cu.Bluetooth-Incoming-Port - n/a
  DEBUG:pygatt.backends.bgapi.util:Checking serial USB device: /dev/cu.usbmodem1 - Low Energy Dongle
  DEBUG:pygatt.backends.bgapi.util:USB device: Low Energy Dongle VID=0x2458 PID=0x0001 on /dev/cu.usbmodem1
  INFO:pygatt.backends.bgapi.bgapi:Found BLED112 on serial port /dev/cu.usbmodem1
  INFO:pygatt.backends.bgapi.bgapi:Resetting and reconnecting to device for a clean environment
  DEBUG:pygatt.backends.bgapi.bgapi:Opening connection to serial port (attempt 1)
  INFO:pygatt.backends.bgapi.bgapi:Auto-detecting serial port for BLED112
  DEBUG:pygatt.backends.bgapi.util:Found 3 serial USB devices
  DEBUG:pygatt.backends.bgapi.util:Checking serial USB device: /dev/cu.SSDC - n/a
  DEBUG:pygatt.backends.bgapi.util:Checking serial USB device: /dev/cu.Bluetooth-Incoming-Port - n/a
  DEBUG:pygatt.backends.bgapi.util:Checking serial USB device: /dev/cu.usbmodem1 - Low Energy Dongle
  DEBUG:pygatt.backends.bgapi.util:USB device: Low Energy Dongle VID=0x2458 PID=0x0001 on /dev/cu.usbmodem1
  INFO:pygatt.backends.bgapi.bgapi:Found BLED112 on serial port /dev/cu.usbmodem1
  DEBUG:pygatt.backends.bgapi.bgapi:Failed to open serial port
  Traceback (most recent call last):
    File "/usr/local/lib/python3.6/site-packages/serial/serialposix.py", line 265, in open
      self.fd = os.open(self.portstr, os.O_RDWR | os.O_NOCTTY | os.O_NONBLOCK)
  OSError: [Errno 6] Device not configured: '/dev/cu.usbmodem1'

  During handling of the above exception, another exception occurred:

  Traceback (most recent call last):
    File "/usr/local/lib/python3.6/site-packages/pygatt/backends/bgapi/bgapi.py", line 159, in _open_serial_port
      timeout=0.25)
    File "/usr/local/lib/python3.6/site-packages/serial/serialutil.py", line 240, in __init__
      self.open()
    File "/usr/local/lib/python3.6/site-packages/serial/serialposix.py", line 268, in open
      raise SerialException(msg.errno, "could not open port {}: {}".format(self._port, msg))
  serial.serialutil.SerialException: [Errno 6] could not open port /dev/cu.usbmodem1: [Errno 6] Device not configured: '/dev/cu.usbmodem1'
  Traceback (most recent call last):
    File "/usr/local/lib/python3.6/site-packages/serial/serialposix.py", line 265, in open
      self.fd = os.open(self.portstr, os.O_RDWR | os.O_NOCTTY | os.O_NONBLOCK)
  OSError: [Errno 6] Device not configured: '/dev/cu.usbmodem1'

  During handling of the above exception, another exception occurred:

  Traceback (most recent call last):
    File "/usr/local/lib/python3.6/site-packages/pygatt/backends/bgapi/bgapi.py", line 159, in _open_serial_port
      timeout=0.25)
    File "/usr/local/lib/python3.6/site-packages/serial/serialutil.py", line 240, in __init__
      self.open()
    File "/usr/local/lib/python3.6/site-packages/serial/serialposix.py", line 268, in open
      raise SerialException(msg.errno, "could not open port {}: {}".format(self._port, msg))
  serial.serialutil.SerialException: [Errno 6] could not open port /dev/cu.usbmodem1: [Errno 6] Device not configured: '/dev/cu.usbmodem1'

  During handling of the above exception, another exception occurred:

  Traceback (most recent call last):
    File "setuputils/testadapter.py", line 13, in <module>
      adapter.start()
    File "/usr/local/lib/python3.6/site-packages/pygatt/backends/bgapi/bgapi.py", line 202, in start
      self._open_serial_port()
    File "/usr/local/lib/python3.6/site-packages/pygatt/backends/bgapi/bgapi.py", line 170, in _open_serial_port
      "No BGAPI compatible device detected")
  pygatt.exceptions.NotConnectedError: No BGAPI compatible device detected
  ```

* Lets fix this now. This happens due to sending a `system reset` command when the adapter starts. We need to disable it. I dont know what the repurcussions are. But until the developers fix it, we can work with the below fix
  1. Open `bgapi.py` file in `pygatt`. In my system it is in `/usr/local/lib/python3.6/site-packages/pygatt/backends/bgapi/bgapi.py`
  2. Comment out the three lines as below (lines 198, 199 and 200). Commented lines are indicated by prefix `#-- ` below:
     ```python
        ...
        # The zero param just means we want to do a normal restart instead of
        # starting a firmware update restart.
        #-- self.send_command(CommandBuilder.system_reset(0))
        #-- self._ser.flush()
        #-- self._ser.close()

        self._open_serial_port()
        ...
     ```
  3. The output should look something like below. The end debug statement is `DEBUG:pygatt.backends.bgapi.bgapi:Received a ResponsePacketType.gap_end_procedure packet: Device in wrong state`. Dont worry about the "wrong state" log. Everything still works
      ```bash
      INFO:pygatt.backends.bgapi.bgapi:Initialized new BGAPI backend
      DEBUG:pygatt.backends.bgapi.bgapi:Opening connection to serial port (attempt 1)
      INFO:pygatt.backends.bgapi.bgapi:Auto-detecting serial port for BLED112
      DEBUG:pygatt.backends.bgapi.util:Found 3 serial USB devices
      DEBUG:pygatt.backends.bgapi.util:Checking serial USB device: /dev/cu.SSDC - n/a
      DEBUG:pygatt.backends.bgapi.util:Checking serial USB device: /dev/cu.Bluetooth-Incoming-Port - n/a
      DEBUG:pygatt.backends.bgapi.util:Checking serial USB device: /dev/cu.usbmodem1 - Low Energy Dongle
      DEBUG:pygatt.backends.bgapi.util:USB device: Low Energy Dongle VID=0x2458 PID=0x0001 on /dev/cu.usbmodem1
      INFO:pygatt.backends.bgapi.bgapi:Found BLED112 on serial port /dev/cu.usbmodem1
      INFO:pygatt.backends.bgapi.bgapi:Resetting and reconnecting to device for a clean environment
      DEBUG:pygatt.backends.bgapi.bgapi:Opening connection to serial port (attempt 1)
      INFO:pygatt.backends.bgapi.bgapi:Auto-detecting serial port for BLED112
      DEBUG:pygatt.backends.bgapi.util:Found 3 serial USB devices
      DEBUG:pygatt.backends.bgapi.util:Checking serial USB device: /dev/cu.SSDC - n/a
      DEBUG:pygatt.backends.bgapi.util:Checking serial USB device: /dev/cu.Bluetooth-Incoming-Port - n/a
      DEBUG:pygatt.backends.bgapi.util:Checking serial USB device: /dev/cu.usbmodem1 - Low Energy Dongle
      DEBUG:pygatt.backends.bgapi.util:USB device: Low Energy Dongle VID=0x2458 PID=0x0001 on /dev/cu.usbmodem1
      INFO:pygatt.backends.bgapi.bgapi:Found BLED112 on serial port /dev/cu.usbmodem1
      INFO:pygatt.backends.bgapi.bgapi:Running receiver
      INFO:pygatt.backends.bgapi.bgapi:Disabling advertising
      DEBUG:pygatt.backends.bgapi.bgapi:Expecting a response of one of [<ResponsePacketType.gap_set_mode: 58>] within 1.000000s
      DEBUG:pygatt.backends.bgapi.bgapi:Received a ResponsePacketType.gap_set_mode packet: Success
      DEBUG:pygatt.backends.bgapi.bgapi:Expecting a response of one of [<ResponsePacketType.sm_set_bondable_mode: 51>] within 1.000000s
      DEBUG:pygatt.backends.bgapi.bgapi:Received a ResponsePacketType.sm_set_bondable_mode packet: Success
      DEBUG:pygatt.backends.bgapi.bgapi:Stopping any outstanding GAP procedure
      DEBUG:pygatt.backends.bgapi.bgapi:Expecting a response of one of [<ResponsePacketType.gap_end_procedure: 61>] within 1.000000s
      DEBUG:pygatt.backends.bgapi.bgapi:Received a ResponsePacketType.gap_end_procedure packet: Device in wrong state
      ```
* Note down the serial port on which the BLED112 is connected. In the above case it is `/dev/cu.usbmodem1`.