from subprocess import call
from util import dict_to_list, ROOT

NETLOGO_HOME = '/opt/netlogo'


def altruism():
    """
    Runs an Altruism experiment for 1000 steps and writes the results to CSV.
    """
    out_path = '%s/temp/altruism_out.csv' % ROOT

    args = {
        '--model': '%s/models/Sample Models/Biology/Evolution/Altruism.nlogo' % NETLOGO_HOME,
        '--setup-file': '%s/data/altruism/experiment.xml' % ROOT,
        '--experiment': 'TestExperiment',
        '--table': out_path,
    }

    print 'Running Altruism model to %s...' % out_path
    call(['%s/netlogo-headless.sh' % NETLOGO_HOME] + dict_to_list(args))

    with open(out_path, 'r') as out_file:
        return out_file.read()
