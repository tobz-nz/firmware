import time, math, config
from machine import Pin, ADC

mtr_enable = Pin('P20', mode=Pin.OUT)
snsr_enable = Pin('P19', mode=Pin.OUT)

adc = ADC()
adc.vref(config.level_vref)
sensor = adc.channel(pin='P13', attn=ADC.ATTN_11DB)

def purge(purge_for = 1):
    """ Purge air from the tube for given number of seconds """

    # turn on the pump for x seconds to purge the pipe
    mtr_enable.toggle()
    time.sleep(purge_for)
    mtr_enable.toggle()


def get():
    """ Take a reading(in mm) from the Level Sensor """

    # turn the sensor on and wait for it to boot up
    snsr_enable.toggle()
    time.sleep(1)

    zero_offset = config.level_zero_offset or 330.00    # Minimum sensor voltage reading (millivolts). In theory should be 330.00 but 286 gives us about 0 so...
    print('Offset = %s' % zero_offset)
    Vsupply = 3300.00       # Supply voltage to sensor (millivolts)
    pmax = 5.00             # Maximum sensor operating range (psi)
    psi_to_pa = 6894.76     # Conversion factor from psi to Pa
    g = 9.81                # Typical gravitational acceleration @ sea level (m/s^2)
    rho = 1000.00           # Density of water (kg/m^3)

    # take a bunch of readings and sum the result
    # this is to metigate the ESP32's noisy ADC
    reading = []
    print('start reading...')
    for i in range(100):
        # Calculate water pressure in Pa
        water_pressure = pmax * psi_to_pa * (sensor.voltage() - zero_offset) / (0.8 * Vsupply)

        # Calculate water depth (mm) from pressure (kPa)
        mm = round((1000 * water_pressure) / (rho * g))

        # append this reading to our list
        reading.append(mm)

        # print(water_pressure)
        print('{}mm'.format(mm))

        # wait a tick for next reading
        time.sleep(0.05) # 0.02 takes ~2 seconds to complete loop

    # turn the sensor off
    snsr_enable.toggle()
    print('end reading')

    rounded = math.ceil(sum(reading)/len(reading))
    reading = rounded if rounded >= 0 else 0

    return reading

def put(last_level):
    """ Store the given level reading """

    file = open(config.last_level_file, 'w')
    file.write('value = %s' % last_level)
    file.close()

def last():
    """ Get the previous level reading """
    output = {}
    try:
        execfile(config.last_level_file, None, output)
        return output['value']
    except:
        return 0
