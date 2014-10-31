from util import ROOT, dict_to_list, call

SUMO_HOME = '/opt/sumo'

SECONDS_IN_HOUR = 60 * 60


def randomHourMinutes_calls(root_path=ROOT):
    calls = []

    net_file = '%s/data/sumo/eich.net.xml' % root_path
    rou_file = '%s/data/sumo/eich.rou.xml' % root_path
    add_file = '%s/data/sumo/eich.add.xml' % root_path

    trip_file = '%s/temp/eich.trip.xml' % root_path
    out_file = '%s/temp/eich.out.xml' % root_path

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


def randomHourMinutes():
    """
    Generates random trips for an hour in Eichstaett, then simulates and outputs minutely.
    """
    calls = randomHourMinutes_calls()
    print 'Generating trips...'
    call(calls[0])
    print 'Running SUMO simulation...'
    return call(calls[1])
