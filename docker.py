import sumo
import altruism
from util import ROOT, call, calls_to_string

SUMO_IMAGE = 'similitude/sumo-simmer'
ALTRUISM_IMAGE = 'quay.io/simmer/netlogo-sample'
# POSTGIS_IMAGE = 'similitude/sumo-simmer'
# IMAGES = [SUMO_IMAGE, ALTRUISM_IMAGE, POSTGIS_IMAGE]
IMAGES = [SUMO_IMAGE, ALTRUISM_IMAGE]


def run_sumo():
    docker_run_all(SUMO_IMAGE, sumo.randomDayHourly_calls('/opt/profile'), opts)


def run_altruism():
    calls = altruism.altruism_calls()
    return docker_run_all(ALTRUISM_IMAGE, calls)


def docker_run_all(image,  calls, opts=[]):
    opts += ['-v', '%s:%s' % (ROOT,ROOT), '--entrypoint', '/bin/sh']
    return docker_run(image, ['-c', '%s' % calls_to_string(calls)], opts)


def docker_run(image, args, opts=[]):
    return call(['sudo', 'docker', 'run'] + opts + [image] + args)
