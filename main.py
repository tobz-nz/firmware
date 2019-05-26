import defaults, level

# load last reading
last_level = level.last()

# Take a new reading
current_level = level.get()

# check if reading needs to be be sent to server
diff = abs(last_level - current_level)
if diff > defaults.level_threshhold:
    # yes it does
    import net, battery

    # connect to network
    net.connect()
    # failed
        # log error
        # sleep
    # send data
    net.post({
        'level': current_level,
        'battery': battery.level(),
        'charging': battery.charging()
    })

    net.disconnect()
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
            # store as last reading
    # no it doesn't
        # sleep
