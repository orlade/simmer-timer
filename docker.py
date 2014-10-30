import sumo
import altruism
from util import call, calls_to_string

SUMO_IMAGE = 'similitude/sumo-simmer'
ALTRUISM_IMAGE = 'quay.io/simmer/netlogo-sample'
# POSTGIS_IMAGE = 'similitude/sumo-simmer'
# IMAGES = [SUMO_IMAGE, ALTRUISM_IMAGE, POSTGIS_IMAGE]
IMAGES = [SUMO_IMAGE, ALTRUISM_IMAGE]


def run_sumo():
    docker_run_all(SUMO_IMAGE, sumo.randomDayHourly_calls())


def run_altruism():
    out_path = '/out.csv'
    calls = altruism.altruism_calls(out_path)
    return docker_run_all(ALTRUISM_IMAGE, calls)


def docker_run_all(image, calls):
    return docker_run(image, ['sh', '-c', '"%s"' % calls_to_string(calls)])


def docker_run(image, args):
    return call(['sudo', 'docker', 'run', image] + args)