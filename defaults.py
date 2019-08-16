from binascii import hexlify
from machine import unique_id

# Level
last_level_file = '/flash/last_level.py'
level_threshhold = 5
zero_offset = 292

# LTE
# lte_apn = 'm2m' # Spark
lte_apn = 'hologram' #Hologram

# Spark band settings
# https://support.m2mone.co.nz/portal/kb/articles/spark-operating-frequencies
# lte_band = 28  ## 700MHz (Spark)

lte_band = 3  ## 1800MHz (Hologram/Vodafone)

# WIFI
wlan_ssid = 'Monkeys'
wlan_pass = 'conspire-la-skeet-roust'

prefered_network = 'lte'

# System
uid = hexlify(unique_id()).decode()
sleep_for = 300 * 1000  # time to deep sleep for in milliseconds
base_url = 'https://dashboard.tankful.nz/api'
update_base_url = 'https://updates.tankful.nz'
ping_limit = 5

device_model = 'UltraTankv2000'
