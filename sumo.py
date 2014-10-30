from util import ROOT, dict_to_list, call

DATA_PATH = '%s/data/sumo' % ROOT
SUMO_HOME = '/opt/sumo'

SECONDS_IN_HOUR = 60 * 60
SECONDS_IN_DAY = SECONDS_IN_HOUR * 24


def randomDayHourly_calls():
    calls = []

    net_file = '%s/eich.net.xml' % DATA_PATH
    rou_file = '%s/eich.rou.xml' % DATA_PATH
    add_file = '%s/eich.add.xml' % DATA_PATH

    trip_file = '%s/temp/eich.trip.xml' % ROOT
    out_file = '%s/temp/eich.out.xml' % ROOT

    trip_generator = '%s/tools/trip/randomTrips.py' % SUMO_HOME
    args = dict_to_list({
        'python': trip_generator,
        '-e': SECONDS_IN_HOUR,
        '-n': net_file,
        '-o': trip_file,
        '-r': rou_file,
    })
    calls.append(args)

    args = {
        '--net-file': net_file,
        '--route-files': rou_file,
        '--additional-files': add_file,
        '--begin': 0,
        '--end': SECONDS_IN_HOUR,
        '--time-to-teleport': 0,
    }
    calls.append(['sumo', '-W'] + dict_to_list(args))
    return calls


def randomDayHourly():
    """
    Generates random trips for a day in Eichstaett, then simulates and outputs hourly.
    """
    calls = randomDayHourly_calls()
    print 'Generating trips...'
    call(calls[0])
    print 'Running SUMO simulation...'
    return call(calls[1])