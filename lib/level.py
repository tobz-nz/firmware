import time, math, defaults
from machine import Pin, ADC

mtr_enable = Pin('P20', mode=Pin.OUT)
snsr_enable = Pin('P19', mode=Pin.OUT)

adc = ADC()
adc.vref(1100)
snsr_data = adc.channel(pin='P13', attn=ADC.ATTN_11DB)

# Default 225
zero_offset = 282

# default 60
kPa = 60

def get(purge_for = 1):
    """ Take a reading(in mm) from the Level Sensor """

    # turn on the pump for x seconds to purge the pipe
    mtr_enable.toggle()
    time.sleep(purge_for)
    mtr_enable.toggle()

    # turn the sensor on and wait for it to boot up
    snsr_enable.toggle()
    time.sleep(1)

    # take a bunch of readings and sum the result
    # this is to metigate the ESP32's noisy ADC
    reading = []
    for i in range(100):
        pkReading = ((snsr_data.voltage() - zero_offset) / kPa)
        mm = pkReading * 100
        reading.append(mm)

        # print(pkReading)
        time.sleep(0.01)

    snsr_enable.toggle()
    rounded = math.ceil(sum(reading)/len(reading))

    reading = rounded if rounded >= 0 else 0

    # store this reading as the "last_leading"
    put(reading)

    return reading

def put(last_level):
    """ Store the given level reading """

    file = open(defaults.last_level_file, 'w')
    file.write('value = %s' % last_level)
    file.close()

def last():
    """ Get the previous level reading """
    output = {}
    execfile(defaults.last_level_file, None, output)
    return output['value']