#!/usr/bin/env python

import sys
sys.path.append(sys.path[0])

from libs.samplebase import SampleBase
from libs.blacklist import *
from libs.config import *
from libs.draw import *


import time
import requests
import threading
import random
import socketio
import eventlet
import eventlet.wsgi

from flask import Flask, render_template

class Feld(SampleBase):
    def __init__(self, *args, **kwargs):
        super(Feld, self).__init__(*args, **kwargs)

        self.parser.add_argument(
            "-s", "--socket",
            action="store_true",
            help="get words from socket")
        self.parser.add_argument(
            '--port',
            nargs=1,
            default=False,
            required=False,
            type=int,
            help="with -s/--socket specify port for connection")
        self.parser.add_argument(
            "--prefix",
            nargs=1,
            default=False,
            required=False,
            help="add prefix",
            type=str)
        self.parser.add_argument(
            "--loader",
            action="store_true",
            help="print loader words")
        self.parser.add_argument(
            '--word',
            nargs=1,
            default=False,
            required=False,
            help="write a word",
            type=str)

        self.args = self.parser.parse_args()

    def run(self):

        # start
        w = self.args.word[0] if self.args.word else "start"
        # print_word(w, self.matrix.CreateFrameCanvas(), self.args.prefix, self.prev_word)
        print "[*] starting..."
        print "data: %s\n" % (w)

        # only loader
        if self.args.loader:
            print "[*] MODE: only loader"
            count = 0
            while True:
                time.sleep(2.0)
                print "data: %s" % (FELD_LOOP[count])
                # print_word(FELD_LOOP[count], self.matrix.CreateFrameCanvas(), self.args.prefix, self.prev_word)
                count = (1 + count) % len(FELD_LOOP)

        # only socket
        if self.args.socket:
            print "[*] MODE: only socket"
            sio = socketio.Server()
            app = Flask(__name__)

            @sio.on('news')
            def message(sid, data):
                print "data: %s" % data
                sio.emit('reply', "received: %s" % data)
                # print_word(data, self.matrix.CreateFrameCanvas(), self.args.prefix, self.prev_word)

            # wrap Flask application with engineio's middleware
            app = socketio.Middleware(sio, app)

            # deploy as an eventlet WSGI server
            eventlet.wsgi.server(eventlet.listen(('', int(self.args.port[0]))), app)

# Main function
if __name__ == "__main__":
    feldman = Feld()
    feldman.run()
