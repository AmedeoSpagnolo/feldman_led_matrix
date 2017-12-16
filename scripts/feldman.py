#!/usr/bin/env python
import sys
import argparse
sys.path.append(sys.path[0])
from libs.liboris import *

class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    pass

parser = argparse.ArgumentParser(
    add_help=True,
    description="Boris Feldman Script by Amedeo Spagnolo",
    epilog="""examples:
    """,
    formatter_class=CustomFormatter)
parser.add_argument(
    '-v',
    '--version',
    action='version',
    version='%(prog)s 1.0')
parser.add_argument(
    '-a',
    '--api',
    action='store_true')

args = parser.parse_args()

print args

if __name__ == "__main__":
    feldman = Feld({"api": False})
    if (not feldman.process()):
        feldman.print_help()
