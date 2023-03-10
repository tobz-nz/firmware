import config, level, tankful, net
from machine import deepsleep

try:
    # load last reading
    last_level = level.last()

    print('Taking reading...')
    current_level = level.get()

    if current_level < last_level:
        # Take a new reading (run pump for x seconds first)
        print('Purging air pipe...')
        level.purge(1)

        # wait for tube pressure to settle
        print('Wait for pressure to stabalize...')
        time.sleep(2)

        # take reading
        print('Taking reading again...')
        current_level = level.get()

    # check if reading needs to be be sent to server
    diff = abs(last_level - current_level)

    print('Levels: {previous}mm -> {current}mm ({diff})'.format(previous=last_level, current=current_level, diff=diff))
    if diff > config.level_threshhold:
        # yes it does
        import power

        # connect to network
        connection, ip = net.connect()
        if connection:
            tankful.register()

            # send data
            response, needs_update = tankful.post('devices/%s/metrics' % config.uid, {
                'value': current_level
            })

            # store latest reading as the "last_leading"
            level.put(current_level)

            # check if firmware needs updating
            if (needs_update[0] is True):
                from OTA import OTA
                updater = OTA()
                updater.update()

            # - crital logs
            # - other logs if in debug mode
            # - previously failed readings
            # success
                # clear previsouly failed readings that succeeded this time
                # check if response has new update header/data
                    # run update process
            # error
                # store reading as unsent - to attempt send again next time

        else:
            print('Failed to connect to network')
            print('Storing level and will attempt to send again later')

    elif tankful.should_ping():
        connection, ip = net.connect()

        # send heartbeat
        successful, response, needsUpdate = tankful.ping()

        # check if firmware needs updating
        if (needsUpdate[0] is True):
            from OTA import OTA
            updater = OTA()
            updater.update()

except Exception as err:
    try:
        print(err)
    except:
        pass

    # log error
    print(err.args[0])
    file = open('/flash/error.log', 'a')
    file.write(err.args[0])
    file.write("\n")
    file.close()

    raise err

finally:
    try:
        # disconnect from network
        net.disconnect(connection)
    except:
        pass

    print('Sleeping for %s minutes' % (config.sleep_for / 60))
    deepsleep(config.sleep_for)
