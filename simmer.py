import httplib
from subprocess import Popen, call
import urllib
from docker import SUMO_IMAGE, ALTRUISM_IMAGE, IMAGES

SIMMER_URL = 'localhost:5000'


def simmer_sumo():
    with open('data/sumo/eich.net.xml') as f:
        invoke(SUMO_IMAGE, 'randomDayHourly', {
            'network': f
        })


def simmer_altruism():
    invoke(ALTRUISM_IMAGE, 'altruism', {
        'altruistic-probability': 0.26,
        'selfish-probability': 0.26,
        'cost-of-altruism': 0.13,
        'benefit-from-altruism': 0.48,
        'disease': 0,
        'harshness': 0,
        'numTicks': 1000,
    })


def simmer_postgis():
    pass


def app(name):
    if name == 'sumo':
        return simmer_sumo
    if name == 'altruism':
        return simmer_altruism
    if name == 'postgis':
        return simmer_postgis
    raise Exception('Unknown app %s' % name)


def invoke(image, service, param_map):
    with httplib.HTTPConnection(SIMMER_URL) as conn:
        params = urllib.urlencode(param_map)
        url = '/services/invoke/%s/%s' % (image, service)
        return conn.request('GET', url, params)


def setup():
    proc = Popen(['../computome/serve.py'], shell=True)

    # Set up the requested images.
    for image in IMAGES:
        conn = httplib.HTTPConnection(SIMMER_URL)
        params = urllib.urlencode({'docker_id': image})
        conn.request('POST', '/services/register', params)

    return proc


def teardown(proc):
    if proc:
        proc.kill()