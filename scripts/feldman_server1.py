#!/usr/bin/env python
# from samplebase import SampleBase
# from rgbmatrix import graphics
import time
import json
import requests
import threading
import random

rbgmatrix = {}
SampleBase = {}

previous_word = ""

# class Feld(SampleBase):
class Feld():
    def __init__(self, *args, **kwargs):
        # super(Feld, self).__init__(*args, **kwargs)
        pass

    def print_on_led_matrix(word, prev_word):

        margin_bottom  = 2
        margin_top = self.matrix.height - 8
        word_length = margin_bottom + ll("FELD" + previous_word)
        prev_word_length = margin_bottom + ll("FELD" + word)
        sign = 1 if (_from < _to) else -1

        while c < steps:

            # line
            line = {}
            line.x0 = margin_bottom + ll("FELD")
            line.y0 = margin_top + 1
            line.x1 = _to + (int((float(abs(_from - _to)) / steps) * (steps - c))) * sign
            line.y1 = margin_top + 1
            line.color = graphics.Color(255,255,255)
            graphics.DrawLine(canvas, line.x0, line.y0, line.x1, line.y1, line.color)

            # dot
            dot = {}
            dot.x = line.x1
            dot.y = margin_top - 1
            dot.col = {"r": 255, "g": 255, "b": 255}
            canvas.SetPixel(dot.x, dot.y, dot.col["r"], dot.col["g"], dot.col["b"])

            # feld
            feld = {}
            feld.x0 = margin_bottom
            feld.y0 = margin_top
            feld.color = graphics.Color(255,255,255)
            graphics.DrawText(canvas, font, feld.x0, feld.y0, feld.color, "FELD")

            # man
            man = {}
            man.x0 = margin_bottom + ll("FELD")
            man.y0 = margin_top - int((float(5) / steps) * (steps - c))
            man.color = graphics.Color(255,255,255)
            graphics.DrawText(canvas, font, man.x0, man.y0, man.color, word)

    def blacklisted(self, word):
        return False if (word in blacklist) else True

    def request(self):
        r = requests.get('http://localhost:8080')
        word = r.content.strip('"')
        if (r.status_code == 200):
            if (self.blacklisted(word) and word != "empty"):
                # time.sleep(2.0)
                threading.Timer(2.0, request).start()
                print_on_led_matrix(word)
            elif(word == "empty"):
                threading.Timer(1.0, request).start()
                print "-"
                print_on_led_matrix(feldloop[random.randint(0,len(feldloop)-1)])
            else:
                print "blacklisted: %s" % word
                request()
        else:
            print "not found!!"

    def run(self):
        print "run"
        # canvas = self.matrix.CreateFrameCanvas()
        #
        # # assets
        # font        = graphics.Font()
        # blacklist   = json.load(open('blacklist.json'))
        # feldloop    = json.load(open('feldloop.json'))
        # font.LoadFont("../fonts/4x6.bdf")
        # max_brightness = self.matrix.brightness
        #
        # def ll(string):
        #     return sum([font.CharacterWidth(ord(c)) for c in string])
        #
        # count = 0
        # word = request()
        # print_on_led_matrix(word)
        #     c += 1
        #     time.sleep(0.01)
        #     canvas = self.matrix.SwapOnVSync(canvas)
        #     canvas.Clear()
        #
        # time.sleep(1.5)
        #
        # count += 1
        # count = count % len(loop)


# Main function
if __name__ == "__main__":
    feldman = Feld()
    if (not feldman.process()):
        feldman.print_help()
