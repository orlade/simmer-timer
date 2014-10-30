import httplib
from subprocess import Popen, call
import urllib

SIMMER_URL = 'localhost:5000'

SUMO_IMAGE = 'similitude/sumo-simmer'
ALTRUISM_IMAGE = 'quay.io/simmer/netlogo-sample'
# POSTGIS_IMAGE = 'similitude/sumo-simmer'
# IMAGES = [SUMO_IMAGE, ALTRUISM_IMAGE, POSTGIS_IMAGE]
IMAGES = [SUMO_IMAGE, ALTRUISM_IMAGE]


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


def setup(images):
    proc = Popen(['../computome/serve.py'], shell=True)

    # Set up the requested images.
    for image in images:
        conn = httplib.HTTPConnection(SIMMER_URL)
        params = urllib.urlencode({'docker_id': image})
        conn.request('POST', '/services/register', params)

    return proc


def teardown(proc):
    if proc:
        proc.kill()