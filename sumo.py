from subprocess import call
from util import ROOT, dict_to_list

DATA_PATH = '%s/data/sumo' % ROOT
SUMO_HOME = '/opt/sumo'

SECONDS_IN_HOUR = 60 * 60
SECONDS_IN_DAY = SECONDS_IN_HOUR * 24


def sumo():
    """
    Generates random trips for a day in Eichstaett, then simulates and outputs hourly.
    """
    net_file = '%s/eich.net.xml' % DATA_PATH
    rou_file = '%s/eich.rou.xml' % DATA_PATH
    add_file = '%s/eich.add.xml' % DATA_PATH

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
