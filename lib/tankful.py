import config
import json
# https://github.com/lucien2k/wipy-urllib
import urequests as requests

def GetToken():
    if not 'API' in globals() :
        try:
            import API

            if API.token is not None:
                return API.token
        except:
            pass

    return None

def register():
    if not 'API' in globals() :
        try:
            import API
            if hasattr(API, 'token'):
                return True
        except:
            pass

    response = requests.post(
        url('devices/%s/token' % config.uid),
        data={ 'model': config.device_model },
        headers={'Accept':'application/json'}
    )

    if response is not None and response.status_code < 300:
        content = json.loads(response.read())
        token = content['api_token']

        file = open('/flash/API.py', 'w')
        file.write('token = "{}"'.format(token))
        file.close()

        import API
        API.token = token
        print('Token: {}'.format(API.token))

        return True, response, check_for_update(response)
    elif response is not None:
        print(response.status_code)
        print(response.read())
    else:
        print('Empty Response')

    return False, None, False


def ping():
    """ Ping the server telling it 'I'm still alive' """

    token = GetToken()
    print('API Token: {}'.format(token))
    if (token is None):
        print('No API Token!')
        return False, None, None

    response = requests.post(
        url('devices/%s/ping' % config.uid),
        headers={'Accept':'application/json'},
        auth=token
    )

    if response is not None:
        return response.status_code >= 200 and response.status_code < 300, response, check_for_update(response)

    return False, response, None


def post(uri, data):
    """ Post new Metric data to server """

    token = GetToken()
    print('API Token: {}'.format(token))
    if (token is None):
        print('No API Token!')
        return None, False

    response = requests.post(
        url('devices/%s/metrics' % config.uid),
        data = data,
        headers={'Accept':'application/json'},
        auth=token
    )

    print(response.status_code)
    print(response.text)

    return response, check_for_update(response)


def should_ping():
    count = 0

    try:
        import PING_COUNT
        count = PING_COUNT.count
    except:
        pass

    print('ping: {}'.format(count))

    file = open('/flash/PING_COUNT.py', 'w')
    if (count >= config.ping_limit):
        file.write('count = {}'.format(0))
        file.close()

        return True
    else:
        file.write('count = {}'.format(count + 1))
        file.close()

        return False


def url(uri):
    import re
    uri = '/' + re.match(r'^\/?(.+)', uri).group(1)

    print('Url: %s' % config.base_url + uri)
    return config.base_url + uri


def check_for_update(response):
    try:
        from OTA_VERSION import VERSION
    except:
        VERSION = '0.0.0'

    if ('X-Current-Firmware' in response.headers):
        version = response.headers['X-Current-Firmware']
        print('current version: {}'.format(VERSION))
        print('latest version: {}'.format(version))
        return version > VERSION, version, VERSION

    return False, None, VERSION
