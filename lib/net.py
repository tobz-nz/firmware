import config
import machine
import time


def connect(type = None):
    """ Connect to network - Try LTE first then fallback to WiFi """

    conectTo = type or config.prefered_network

    if (conectTo is 'lte'):
        try:
            return connect_lte()
        except:
            pass

        return connect_wlan()
    else:
        try:
            return connect_wlan()
        except:
            pass

        return connect_lte()

def disconnect(connection):
    """ Disconnect from the provided network """

    connection.disconnect()

    # LTE needs to be dettached as well as disconnected
    if (hasattr(connection, 'dettach')):
        connection.dettach()
        print('Detached')

    print('Disconnected')
    return True


def connect_lte():
    """ Connect to LTE network """

    from network import LTE

    connection = LTE(carrier='standard')

    print('Connecting to LTE...')
    print('attaching ', end='')
    i = 0
    connection.attach(band=config.lte_band, apn=config.lte_apn)
    while not connection.isattached():
        i = i+1
        machine.idle()  # save power while waiting
        print('.', end='')
        if (i > 50):
            print('Timeout')
            return None, None
    print('')
    print('Attached')

    print('Connecting', end='')
    connection.connect()
    i = 0
    while not connection.isconnected():
        i = i+1
        machine.idle()  # save power while waiting
        print('.', end='')
        if (i > 50):
            print('Timeout')
            return None, None

    print('')
    print('Connected')

    return connection, None


def connect_wlan():
    """ Connect to WiFi network """

    try:
        from network import WLAN
        import WIFI
        print('Connecting to WiFi...')
        connection = WLAN(mode=WLAN.STA, power_save=True)
        connection.connect(WIFI.wlan_ssid, auth=(WLAN.WPA2, WIFI.wlan_pass), timeout=5000)

        while not connection.isconnected():
            machine.idle()  # save power while waiting

        print('Connected')
        return connection, connection.ifconfig()[0]
    except:
        print('No WIFI credentials found')
        pass



def at(connection, cmd):
    """ Send an AT command to the modem """
    response = connection.send_at_cmd(cmd).split('\r\n')
    for line in response:
        print(line)


def debug(connection):
    """ Print debug details about the modem & connect to the console """

    import sqnsupgrade

    at(connection, 'ATI1')  # Software Version
    at(connection, 'AT!="fsm"')  # get the System FSM
    at(connection, 'AT!="showphy"')  # Fet the PHY status
    at(connection, 'AT+CSQ')  # Signal quality

    sqnsupgrade.info()  # modem firmware info
