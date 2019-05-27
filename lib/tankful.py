import defaults
from http import MicroWebCli as HTTP


def register():
    request = HTTP('%s/devices/%s/token' % (defaults.base_url, defaults.uid))
    request.OpenRequest(contentType='application/json')
    response = request.GetResponse()
    print(response.ReadContentAsJSON())


def ping():
    return HTTP.POSTRequest('%s/devices/%s/ping' % (
        defaults.base_url,
        defaults.uid
    )).IsSuccess()


def post(url, data):
    r = HTTP.GETRequest('http://google.com').GetResponse()

    print(r.text)

    return True


def should_ping():
    return False
