from subprocess import call
from util import ROOT, dict_to_list

SUMO_HOME = '/opt/sumo'

SECONDS_IN_HOUR = 60 * 60
SECONDS_IN_DAY = SECONDS_IN_HOUR * 24


def sumo():
    """
    Generates random trips for a day in Eichstaett, then simulates and outputs hourly.
    """
    net_file = '%s/data/eich.net.xml' % ROOT
    rou_file = '%s/data/eich.rou.xml' % ROOT
    add_file = '%s/data/eich.add.xml' % ROOT

    trip_file = '%s/temp/eich.trip.xml' % ROOT
    out_file = '%s/temp/eich.out.xml' % ROOT

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
