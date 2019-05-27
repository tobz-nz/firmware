from binascii import hexlify
from machine import unique_id

# Level
last_level_file = '/flash/last_level.py'
level_threshhold = 5

# LTE
lte_apn = 'm2m'

# Spark band settings
# https://support.m2mone.co.nz/portal/kb/articles/spark-operating-frequencies
lte_band = 28  ## 700MHz (not 1800MHz)

# WIFI
wlan_ssid = 'Monkeys'
wlan_pass = 'conspire-la-skeet-roust'

# System
uid = hexlify(unique_id()).decode()
sleep_for = 300 * 1000  # time to deep sleep for in milliseconds
base_url = 'https://app.tankful.nz/api'
