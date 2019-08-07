import defaults
from http import MicroWebCli as HTTP


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

            if API.token is not None:
                return True
        except:
            pass

    response = HTTP.JSONRequest(url('devices/%s/token' % defaults.uid), 'POST', { 'model': defaults.device_model })

    if type(response) is HTTP._response:
        print(response)
        print(response.GetStatusCode())
        print(response.GetContentType())
        print(response.GetContentLength())
        print(response.GetHeaders())
        print(response.ReadContent())
        print(response.ReadContentAsJSON())

        responseBody = response.ReadContentAsJSON()
        if responseBody is not None:
            token = response.ReadContentAsJSON()['api_token']

            file = open('/flash/API.py', 'w')
            file.write('token = {}'.format(token))
            file.close()

            import API
            API.token = token
            print('Token: {}'.format(API.token))

        return (responseBody is not None), response, check_for_update(response)

    elif response is not None:
        print(response)
        print(response.ReadContentAsJSON())
        print(response.ReadContent())
        print(response.GetHeaders())
        print('(%s) %s' % (response.GetStatusCode(), response.GetStatusMessage()))

        return False, response, check_for_update(response)
    else:
        print('Empty Response')
        return False



def ping():
    token = GetToken()
    response = HTTP.JSONRequest(url('devices/%s/ping' % defaults.uid), 'POST', auth=HTTP.AuthToken(token))

    if response is not None:
        return response.GetStatusCode() >= 200 and response.GetStatusCode() < 300, response, check_for_update(response)

    return False, response


def post(uri, data):
    token = GetToken()
    response = HTTP.JSONRequest(url('devices/%s/metrics' % defaults.uid), 'POST', data, auth=HTTP.AuthToken(token))

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
    if (count >= defaults.ping_limit):
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

    print('Url: %s' % defaults.base_url + uri)
    return defaults.base_url + uri


def check_for_update(response):
    from OTA_VERSION import VERSION
    if ('X-Current-Firmware' in response.GetHeaders()):
        version = response.GetHeaders()['X-Current-Firmware']
        return VERSION < version, version, VERSION

    return False
