import os
import sys

ROOT = os.path.abspath(os.path.dirname(sys.argv[0]))

def dict_to_list(d):
    return reduce(lambda xs, x: xs + map(str, x), map(list, d.items()), [])