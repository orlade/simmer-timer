import os
import sys
import subprocess

ROOT = os.path.abspath(os.path.dirname(sys.argv[0]))

def dict_to_list(d):
    items = reduce(lambda xs, (k, v): xs + [k, v], d.items(), [])
    return map(str, filter(lambda x: x is not None, items))

def quote_space(s):
    return '"%s"' % s if ' ' in s else s

def args_to_string(args):
    return ' '.join(map(quote_space, map(str, args)))

def calls_to_string(calls):
    return ' && '.join(map(args_to_string, calls))

def call(args):
    print ' >>> $ %s' % args
    return subprocess.call(args)
