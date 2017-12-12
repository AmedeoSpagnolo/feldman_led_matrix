#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
import time
import json
import requests
import threading
import random

prev_word = ""

class Feld(SampleBase):
    def __init__(self, *args, **kwargs):
        super(Feld, self).__init__(*args, **kwargs)
        canvas      = self.matrix.CreateFrameCanvas()
        blacklist   = json.load(open('blacklist.json'))
        feldloop    = json.load(open('feldloop.json'))
        font        = graphics.Font()
        anim_time   = 100

    def print_word(word):

        def ll(string):
            return sum([font.CharacterWidth(ord(c)) for c in string])

        count   = 0
        font    = self.font
        canvas  = self.convas

        margin_bottom   = 2
        margin_top      = self.matrix.height - 8
        word_length     = margin_bottom + ll("FELD" + word)
        prev_word_len   = margin_bottom + ll("FELD" + prev_word)
        sign = 1 if (prev_word_len < word_length) else -1

        font.LoadFont("../fonts/4x6.bdf")

        while c < anim_time:
            canvas.Clear()

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

            c += 1
            time.sleep(0.01)

            canvas = self.matrix.SwapOnVSync(canvas)

        prev_word = word

    def isblacklisted(self,word):
        return True if (word in self.blacklist) else False

    def get_word_from_list():
        return self.feldloop[random.randint(0,len(self.feldloop)-1)]

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
        temp = self.get_word_from_api("http://localhost:8080")
        word = temp if (temp and temp != None) else self.get_word_from_list()
        print_word(word)
        threading.Timer(2.0, run).start()

# Main function
if __name__ == "__main__":
    feldman = Feld()
    if (not feldman.process()):
        feldman.print_help()
