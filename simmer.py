from subprocess import Popen, call
import requests
import time
from urllib import urlencode
from docker import SUMO_IMAGE, ALTRUISM_IMAGE, IMAGES

SIMMER_URL = 'http://localhost:5000'


def simmer_sumo():
    with open('data/sumo/eich.net.xml') as f:
        invoke('SumoService', 'randomHourMinutes', {}, {
            '__file__network': f
        })


def simmer_altruism():
    invoke('NetLogoService', 'altruism', {
        'altruisticProbability': 0.26,
        'selfishProbability': 0.26,
        'altruismCost': 0.13,
        'altruismBenefit': 0.48,
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


def invoke(image, service, param_map, file_map=None):
    url = '%s/packages/%s/%s/invoke' % (SIMMER_URL, image, service)
    return requests.post(url, params=param_map, files=file_map)


def setup():
    #proc = Popen(['../computome/serve.py'], shell=True)
    #time.sleep(1)

    # Set up the requested images.
    for image in IMAGES:
        requests.post('%s/packages/register' % SIMMER_URL, params={'docker_id': image})

    #return proc


def teardown(proc):
    if proc:
        proc.kill()
