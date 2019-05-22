# boot.py -- run on boot-up
import os
import time
# import config
import pycom
from machine import UART
from network import Bluetooth, WLAN

try:
    import LTE
except Exception:
    pass

uart = UART(0, 115200)
os.dupterm(uart)

# don't boot up wifi AP (ctrl+f in console safe boot with AP)
pycom.wifi_on_boot(False)

# disable wifi
WLAN().deinit()

# disable bluetooth
Bluetooth().deinit()

# try:
#     # disable LTE (really slow for some reason? oh and fails anyway?)
#     LTE().deinit()
# except Exception:
#     pass
