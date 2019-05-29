import defaults
from http import MicroWebCli as HTTP


def register():
    response = HTTP.JSONRequest(url('devices/%s/token' % defaults.uid), 'POST', { 'model': 'UltraTankv2000'})
    if response is not None:
        print(response.ReadContentAsJSON())
        print(response.ReadContent())
        print(response.GetHeaders())
        print('(%s) %s' % (response.GetStatusCode(), response.GetStatusMessage()))

        responseData = response.ReadContentAsJSON()
        if response.IsSuccess() and responseData is not None:
            # get API token and save to disk for easy access
            file = open('/flash/API', 'w')
            file.write('token = %s' % responseData.data.api_token)
            file.close()

            return True

        print(responseData)
        return False
    else:
        print('(%s) %s' % (response.GetStatusCode(), response.GetStatusMessage()))



def ping():
    response = HTTP.JSONRequest(url('devices/%s/ping' % defaults.uid), o={})
    if response is not None:
        return response.IsSuccess()
    else:
        print('(%s) %s' % (response.GetStatusCode(), response.GetStatusMessage()))

    return False


def post(uri, data):
    r = HTTP.GETRequest(url(uri)).GetResponse()

    print(r.ReadContentAsJSON)

    return True


def should_ping():
    return False


def url(uri):
    import re
    uri = '/' + re.match(r'^\/?(.+)', uri).group(1)

    print('Url: %s' % defaults.base_url + uri)
    return defaults.base_url + uri
