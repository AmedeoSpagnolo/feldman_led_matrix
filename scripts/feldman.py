#!/usr/bin/env python
import sys
sys.path.append(sys.path[0])
from libs.liboris import *

if __name__ == "__main__":
    feldman = Feld({"api": False})
    if (not feldman.process()):
        feldman.print_help()
