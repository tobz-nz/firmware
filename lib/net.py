import defaults
import machine
import time
from http import MicroWebCli as HTTP

base_url = 'https://app.tankful.nz/api'


def connect():
    try:
        return lte()
    except Exception:
        print('LTE failed')

        try:
            return wlan()
        except Exception:
            print('WiFi failed')
            return False

    return True

def disconnect(connection):
    connection.disconnect()

    # LTE needs to be disconnected as well
    if (hasattr(connection, 'dettach')):
        connection.dettach()

    print('Disconnected')
    return True


def lte():
    from network import LTE

    connection = LTE(carrier='standard')

    print('attaching ', end='')
    i = 0
    connection.attach(band=defaults.lte_band, apn=defaults.lte_apn)
    while not connection.isattached():
        i = i+1
        machine.idle()  # save power while waiting
        print('.', end='')
        if (i > 50):
            print('Timeout')
            return connection
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
            return connection

    print('')
    print('Connected')

    return connection


def wlan():
    from network import WLAN

    connection = WLAN(mode=WLAN.STA, power_save=True)
    connection.connect(defaults.wlan_ssid, auth=(
        WLAN.WPA2,
        defaults.wlan_pass
    ))

    while not connection.isconnected():
        machine.idle()  # save power while waiting

    return connection.ifconfig()[0]


def register():
    request = HTTP('%s/devices/%s/token' % (base_url, defaults.uid))
    request.OpenRequest(contentType='application/json')
    response = request.GetResponse()
    print(response.ReadContentAsJSON())


def ping():
    return HTTP.PostRequest('%s/devices/%s/ping' % (base_url, )).IsSuccess()


def post(url, data):
    r = HTTP.GetRequest('http://google.com').GetResponse()

    print(r.text)
    connection.disconnect()

    return True


def at(connection, cmd):
    response = connection.send_at_cmd(cmd).split('\r\n')
    for line in response:
        print(line)


def debug(connection):
    import sqnsupgrade

    at(connection, 'ATI1')  # Software Version
    at(connection, 'AT!="fsm"')  # get the System FSM
    at(connection, 'AT!="showphy"')  # Fet the PHY status
    at(connection, 'AT+CSQ')  # Signal quality

    sqnsupgrade.info()  # modem firmware info
