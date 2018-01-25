#!/usr/bin/env python
import sys
sys.path.append(sys.path[0])
from libs.samplebase import SampleBase
from rgbmatrix import graphics
import time
import json
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
            "-a", "--api",
            action="store_true",
            help="get words from api")
        self.parser.add_argument(
            "-s", "--socket",
            action="store_true",
            help="get words from socket")
        self.parser.add_argument(
            "--boris",
            action="store_true",
            help="boris script")
        self.parser.add_argument(
            '--port',
            nargs=1,
            default=False,
            required=False)
        self.parser.add_argument(
            '--write',
            nargs=1,
            default=False,
            required=False)
        self.parser.add_argument(
            '--ip',
            nargs=1,
            default=False,
            required=False)

        self.blacklist   = json.load(open('assets/datasets/blacklist.json'))
        self.feldloop    = json.load(open('assets/datasets/feldloop.json'))
        self.font        = graphics.Font()
        self.anim_time   = 15
        self.prev_word   = ""
        self.args        = self.parser.parse_args()
        self.api         = self.args.api
        self.socket         = self.args.socket

        if self.api and self.args.ip and self.args.port:
            self.url = "http://" + self.args.ip[0] + ":" + self.args.port[0]

    def print_word(self, word, canvas):

        def ll(string):
            return sum([font.CharacterWidth(ord(c)) for c in string])

        c   = 0
        font    = self.font

        margin_bottom   = 2
        margin_top      = self.matrix.height - 8
        word_length     = margin_bottom + ll("FELD" + word)
        prev_word_len   = margin_bottom + ll("FELD" + self.prev_word)
        steps           = self.anim_time
        sign            = 1 if (prev_word_len < word_length) else -1

        self.matrix.brightness = 50
        font.LoadFont("assets/fonts/4x6.bdf")

        while (c < steps):
            canvas.Clear()

            # line
            l = {
                "x0": margin_bottom + ll("FELD"),
                "y0": margin_top + 1,
                "x1": word_length + (int((float(abs(prev_word_len - word_length)) / steps) * (steps - c))) * sign,
                "y1": margin_top + 1,
                "color": graphics.Color(255,255,255)
            }
            graphics.DrawLine(canvas, l["x0"], l["y0"], l["x1"], l["y1"], l["color"])

            # dot
            d = {
                "x": l["x1"],
                "y": margin_top - 1,
                "col": {"r": 255, "g": 255, "b": 255}
            }
            canvas.SetPixel(d["x"], d["y"], d["col"]["r"], d["col"]["g"], d["col"]["b"])

            # feld
            f = {
                "x0": margin_bottom,
                "y0": margin_top,
                "color": graphics.Color(255,255,255)
            }
            graphics.DrawText(canvas, font, f["x0"], f["y0"], f["color"], "FELD")

            # man
            m = {
                "x0": margin_bottom + ll("FELD"),
                "y0": margin_top - int((float(5) / steps) * (steps - c)),
                "color": graphics.Color(255,255,255)
            }
            graphics.DrawText(canvas, font, m["x0"], m["y0"], m["color"], word)

            c += 1
            time.sleep(0.01)

            canvas = self.matrix.SwapOnVSync(canvas)

        self.prev_word = word

    def isblacklisted(self, sentence):
        if (any([ (i in " ".join(self.blacklist)) for i in sentence.split()])):
            return False
        else:
            return True

    def get_word_from_list(self, arr):
        return arr[random.randint(0,len(arr)-1)]

    def get_word_from_api(self, url):
        try:
            r = requests.get(url)
            word = r.content[1:-1]
            if (self.isblacklisted(word)):
                return word
            else:
                print "blacklisted: %s" % word
                return False
        except requests.exceptions.RequestException as e:
            print e
            return False

    def run(self):
        if self.args.boris:
            if self.api:
                temp = self.get_word_from_api(self.url)
                word = temp if (temp and temp != None) else self.get_word_from_list(self.feldloop)
                self.print_word(word, self.matrix.CreateFrameCanvas())
                threading.Timer(2.0, self.run).start()
            elif self.socket:
                # do something
                sio = socketio.Server()
                app = Flask(__name__)

                @sio.on('news')
                def message(sid, data):
                    print "data: %s" % data
                    sio.emit('reply', "received: %s" % data)
                    self.print_word(data, self.matrix.CreateFrameCanvas())

                if __name__ == '__main__':
                    app = socketio.Middleware(sio, app) # wrap Flask application with engineio's middleware
                    eventlet.wsgi.server(eventlet.listen(('', int(self.args.port))), app) # deploy as an eventlet WSGI server

            else:
                count = 0
                while True:
                    time.sleep(2.0)
                    self.print_word(self.feldloop[count], self.matrix.CreateFrameCanvas())
                    count = (1 + count) % len(self.feldloop)
        elif self.args.write:

            self.print_word(self.args.write, self.matrix.CreateFrameCanvas())
        else:
            font = graphics.Font()
            font.LoadFont("assets/fonts/4x6.bdf")
            print dir(self.matrix)
            while True:
                m = {
                    "text":     "boris",
                    "x0":       2,
                    "y0":       self.matrix.height,
                    "canvas":   self.matrix.CreateFrameCanvas(),
                    "color":    graphics.Color(255,255,255)}
                graphics.DrawText(m["canvas"], font, m["x0"], m["y0"], m["color"], m["text"])
                m["canvas"] = self.matrix.SwapOnVSync(m["canvas"])

# Main function
if __name__ == "__main__":
    feldman = Feld()
    if (not feldman.process()):
        feldman.print_help()
