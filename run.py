#!/usr/bin/python
"""
Simple performance profiling script.
"""
import math
import os
from datetime import datetime
from distutils.dir_util import mkpath
from timeit import default_timer as timer

from altruism import altruism
import simmer
from sumo import sumo


def profile(function, iterations=1, write=True):
    def inner(i):
        print ' >>> START %s ITERATION %d' % (function.__name__, i)
        start = timer()
        function()
        delta = timer() - start
        print ' >>> ITERATION %d COMPLETE (%d s)' % (i, delta)
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
        fname = 'results/%s-%s.txt' % (function.__name__, datetime.now().isoformat())
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

    profile(sumo, 10)
    profile(altruism, 10)

    proc = simmer.setup()

    profile(simmer.app('sumo'))
    profile(simmer.app('altruism'))

    simmer.teardown(proc)

    clean_temp()

