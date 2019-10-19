from binascii import hexlify
from machine import unique_id

# Level
last_level_file = '/flash/LAST_LEVEL.py'

# mm threshold between readings.
# If the reading is +/- within this threshold from
# the previous reading, it is ignored
level_threshhold = 15

# LTE
# lte_apn = 'm2m' # Spark
lte_apn = 'hologram' # Hologram

# Spark band settings
# https://support.m2mone.co.nz/portal/kb/articles/spark-operating-frequencies
# lte_band = 28  ## 700MHz (Spark)

lte_band = 3  ## 1800MHz (Hologram/Vodafone)

prefered_network = 'wlan'

# System
uid = hexlify(unique_id()).decode()
# time to deep sleep for in milliseconds
sleep_for = 900 * 1000 # 15 minutes
base_url = 'https://dashboard.tankful.nz/api'
update_base_url = 'https://updates.tankful.nz'
ping_limit = 4 * 12 # about 12 hours

device_model = 'UltraTankv2000'
