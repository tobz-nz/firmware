import defaults, level, tankful, net
from machine import deepsleep

try:

    # load last reading
    last_level = level.last()

    # Take a new reading (run pump for x seconds first)
    level.purge(0.5)
    current_level = level.get()

    print('Levels: {previous} / {current}'.format(previous=last_level, current=current_level))

    # check if reading needs to be be sent to server
    diff = abs(last_level - current_level)
    if diff > defaults.level_threshhold:
        # yes it does
        import power

        # connect to network
        connection, ip = net.connect()
        if connection:
            tankful.register()

            # send data
            response, needs_update = tankful.post('devices/%s/metrics' % defaults.uid, {
                'value': current_level,
                'battery': power.level(),
                'charging': power.is_charging()
            })

            # check if firmware needs updating
            if (needs_update is True):
                from OTA import OTA
                OTA.update()

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

    elif tankful.should_ping():
        connection, ip = net.connect()

        # send heartbeat
        successful, response = tankful.ping()

        # check if firmware needs updating
        if (tankful.check_for_update(response) is True):
            from OTA import OTA
            OTA.update()

        net.disconnect(connection)

except Exception as err:
    try:
        net.disconnect(connection)
    except:
        pass

    # log error
    print(err.args[0])
    file = open('/flash/error.log', 'a')
    file.write(err.args[0])
    file.write("\n")
    file.close()

finally:
    print('Sleeping for %s' % defaults.sleep_for)
    deepsleep(defaults.sleep_for)
