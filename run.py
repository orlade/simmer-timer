#!/usr/bin/python
"""
Simple performance profiling script.
"""
import math
import os
import time
from datetime import datetime
from distutils.dir_util import mkpath
from timeit import default_timer as timer

from altruism import altruism
from sumo import randomHourMinutes
from world import cityLanguage
import docker
import simmer


def profile(function, iterations=1, delay=0, write=True):
    def inner(i):
        print ' >>> START %s ITERATION %d' % (function.__name__, i)
        start = timer()
        function()
        delta = timer() - start
        print ' >>> ITERATION %d COMPLETE (%d s)' % (i, delta)
        if delay:
            print 'Sleeping for %d...' % delay
            time.sleep(delay)
        return delta

    times = map(inner, xrange(iterations))

    average = lambda xs: float(sum(xs)) / len(xs)
    data = {
        'times': times,
        'avg': average(times),
        'min': min(times),
        'max': max(times),
    }
    data['var'] = average(map(lambda x: (x - data['avg']) ** 2, times))
    data['stdev'] = math.sqrt(data['var'])

    if write:
        mkpath('results')
        suffix = datetime.now().isoformat().replace(':', '_')
        fname = 'results/%s-%s.txt' % (function.__name__, suffix)
        with open(fname, 'w') as f:
            f.write('\n'.join(map(str, data.items())))

    return data


def clean_temp():
    print 'Cleaning temp directory...'
    for f in os.listdir('temp'):
        path = os.path.join('temp', f)
        print 'Removing %s...' % path
        os.remove(path)

    other = ['data/eich.rou.alt.xml']
    map(os.remove, filter(os.path.isfile, other))


if __name__ == '__main__':
    mkpath('temp')

    #profile(randomHourMinutes, 10)
    #profile(altruism, 10)
    #profile(cityLanguage, 10)

    #profile(docker.run_sumo, 10)
    #profile(docker.run_altruism, 10)
    #profile(docker.run_world, 10)

    proc = simmer.setup()

    #try:
    #profile(simmer.app('sumo'), 10, 3)
    #profile(simmer.app('altruism'), 10, 2)
    profile(simmer.app('world'), 10, 2)
    #finally:
     #   simmer.teardown(proc)

    clean_temp()

