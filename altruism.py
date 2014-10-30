from util import dict_to_list, ROOT, call

NETLOGO_HOME = '/opt/netlogo'

DEFAULT_OUT_PATH = '%s/temp/altruism_out.csv' % ROOT

def altruism_calls(out_path=DEFAULT_OUT_PATH):
    calls = []
    args = {
        '--model': '%s/models/Sample Models/Biology/Evolution/Altruism.nlogo' % NETLOGO_HOME,
        '--setup-file': '%s/data/altruism/experiment.xml' % ROOT,
        '--experiment': 'TestExperiment',
        '--table': out_path,
    }
    calls.append(['%s/netlogo-headless.sh' % NETLOGO_HOME] + dict_to_list(args))
    calls.append(['cat', out_path])
    return calls

def altruism():
    """
    Runs an Altruism experiment for 1000 steps and writes the results to CSV.
    """
    calls = altruism_calls(DEFAULT_OUT_PATH)
    print 'Running Altruism model to %s...' % DEFAULT_OUT_PATH
    return map(call, calls)[-1]
