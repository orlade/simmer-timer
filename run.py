#!/usr/bin/python
"""
Simple performance profiling script.
"""
from distutils.dir_util import mkpath
import os
import sys
from subprocess import call
from timeit import default_timer as timer
import math
from datetime import date

SECONDS_IN_HOUR = 60 * 60
SECONDS_IN_DAY = SECONDS_IN_HOUR * 24

SUMO_HOME = '/opt/sumo'


def dict_to_list(d):
    return reduce(lambda xs, x: xs + map(str, x), map(list, d.items()), [])


def sumo():
    """
    Generates random trips for a day in Eichstaett, then simulates and outputs hourly.
    """
    net_file = '%s/data/eich.net.xml' % root
    rou_file = '%s/data/eich.rou.xml' % root
    add_file = '%s/data/eich.add.xml' % root

    trip_file = '%s/temp/eich.trip.xml' % root
    out_file = '%s/temp/eich.out.xml' % root

    print 'Generating trips to %s...' % trip_file
    trip_generator = '%s/tools/trip/randomTrips.py' % SUMO_HOME
    args = {
        'python': trip_generator,
        '-e': str(SECONDS_IN_DAY),
        '-n': net_file,
        '-o': trip_file,
        '-r': rou_file,
    }
    call(dict_to_list(args))

    print 'Running SUMO simulation to %s...' % out_file
    args = {
        '--net-file': net_file,
        '--route-files': rou_file,
        '--additional-files': add_file,
        '--begin': 0,
        '--end': 1,
        '--time-to-teleport': -1,
    }
    call(['sumo', '-W'] + dict_to_list(args))


def profile(function, iterations=1, write=True):
    def inner(_):
        start = timer()
        function()
        return timer() - start

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
        with open('results/%s.txt' % date.today().isoformat(), 'w') as f:
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
    root = os.path.abspath(os.path.dirname(sys.argv[0]))

    profile(sumo, 10)

    clean_temp()

