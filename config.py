from binascii import hexlify
from machine import unique_id
import WIFI

# Level
last_level_file = '/flash/last_level.py'

# mm threshold between readings.
# If the reading is +/- within this threshold from
# the previous reading, it is ignored
level_threshhold = 10

# LTE
# lte_apn = 'm2m' # Spark
lte_apn = 'hologram' # Hologram

# Spark band settings
# https://support.m2mone.co.nz/portal/kb/articles/spark-operating-frequencies
# lte_band = 28  ## 700MHz (Spark)

lte_band = 3  ## 1800MHz (Hologram/Vodafone)

# WIFI
wlan_ssid = WIFI.wlan_ssid
wlan_pass = WIFI.wlan_pass

prefered_network = 'wlan'

# System
uid = hexlify(unique_id()).decode()
sleep_for = 300 * 1000  # time to deep sleep for in milliseconds
base_url = 'https://dashboard.tankful.nz/api'
update_base_url = 'https://updates.tankful.nz'
ping_limit = 5

device_model = 'UltraTankv2000'
