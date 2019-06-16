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

        token = response.ReadContentAsJSON()['api_token']

        file = open('/flash/API.py', 'w')
        file.write('token = \'%s\'' % token)
        file.close()

        import API
        API.token = token

        return True, response

    elif response is not None:
        print(response)
        print(response.ReadContentAsJSON())
        print(response.ReadContent())
        print(response.GetHeaders())
        print('(%s) %s' % (response.GetStatusCode(), response.GetStatusMessage()))

        return False, response
    else:
        print('Empty Response')
        return False



def ping():
    token = GetToken()
    response = HTTP.JSONRequest(url('devices/%s/ping' % defaults.uid), 'POST', auth=HTTP.AuthToken(token))

    if response is not None:
        return response.GetStatusCode() >= 200 and response.GetStatusCode() < 300, response

    return False, response


def post(uri, data):
    token = GetToken()
    response = HTTP.JSONRequest(url('devices/%s/metrics' % defaults.uid), 'POST', data, auth=HTTP.AuthToken(token))

    return response


def should_ping():
    return False


def url(uri):
    import re
    uri = '/' + re.match(r'^\/?(.+)', uri).group(1)

    print('Url: %s' % defaults.base_url + uri)
    return defaults.base_url + uri
