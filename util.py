import os
import sys
import subprocess

ROOT = os.path.abspath(os.path.dirname(sys.argv[0]))

def dict_to_list(d):
    return reduce(lambda xs, x: xs + map(str, x), map(list, d.items()), [])

def quote_space(s):
    return '"%s"' % s if ' ' in s else s

def args_to_string(args):
    return ' '.join(map(quote_space, map(str, args)))

def calls_to_string(calls):
    return ' && '.join(map(args_to_string, calls))

def call(args):
    print ' >>> $ %s' % args
    return subprocess.call(args)
