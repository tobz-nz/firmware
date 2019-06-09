import defaults, level, tankful
from machine import deepsleep

try:

    # load last reading
    last_level = level.last()

    # Take a new reading
    current_level = level.get()

    print('Levels: {previous} / {current}'.format(previous=last_level, current=current_level))

    # check if reading needs to be be sent to server
    diff = abs(last_level - current_level)
    if diff > defaults.level_threshhold:
        # yes it does
        import net, power

        # connect to network
        connection = net.connect()
        if connection:
            # send data
            tankful.post('devices/%s/metrics' % defaults.uid, {
                'level': current_level,
                'battery': power.level(),
                'charging': power.is_charging()
            })
            # - reading value
            # - battery level
            # - battery charging status

                # - crital logs
                # - other logs if in debug mode
                # - previously failed readings
                # success
                    # clear previsouly failed readings that succeeded this time
                    # check if response has new update header/data
                        # run update process
                # error
                    # store reading as unsent - to attempt send again next time

            net.disconnect(connection)
        else:
            print('Failed to connect to network')
            print('Storing level and will attempt to send again later')

                # store as last reading
        # no it doesn't
            # sleep
    elif tankful.should_ping():
        connection = net.connect()
        tankful.ping()
        net.disconnect(connection)

except Exception as err:
    # log error
    print(err.args[0])
    file = open('/flash/error.log', 'a')
    file.write(err.args[0])
    file.close()

finally:
    print('Sleeping for %s' % defaults.sleep_for)
    # deepsleep(defaults.sleep_for)
