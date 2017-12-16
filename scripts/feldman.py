#!/usr/bin/env python
import sys
sys.path.append(sys.path[0])
from libs.liboris import *

opt = {
    "api": False, # False ==> simple Feldman loader
    "ip": "localhost",
    "port": 8080}

if __name__ == "__main__":
    feldman = Feld(opt)
    if (not feldman.process()):
        feldman.print_help()


# "http://192.168.43.155:8080"
