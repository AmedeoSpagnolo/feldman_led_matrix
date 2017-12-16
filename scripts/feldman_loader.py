#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
import time
import json
import argparse

class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    pass

parser = argparse.ArgumentParser(
    add_help=False,
    formatter_class=CustomFormatter)
parser.add_argument(
    '-v',
    '--version',
    action='version',
    version='%(prog)s 1.0')
parser.add_argument(
    '-s',
    '--simple_loader',
    action='store_true')
parser.add_argument(
    '-c',
    '--call_api',
    action='store_true')

args = parser.parse_args()

class Feld(SampleBase, obj = {}):
    def __init__(self, *args, **kwargs):
        super(Feld, self).__init__(*args, **kwargs)
        print obj

    def run(self):
        canvas = self.matrix.CreateFrameCanvas()

        # assets
        red     = graphics.Color(255, 0, 0)
        green   = graphics.Color(0, 255, 0)
        blue    = graphics.Color(0, 0, 255)
        white   = graphics.Color(255,255,255)
        font    = graphics.Font()
        loop    = json.load(open('feldloop.json'))
        font.LoadFont("../fonts/4x6.bdf")
        max_brightness = self.matrix.brightness

        count       = 0
        marginleft  = 2
        margintop   = 10

        def ll(string):
            return sum([font.CharacterWidth(ord(c)) for c in string])

        while True:
            c = 0
            steps = 20
            _from   = marginleft + ll("FELD" + loop[(count - 1) + count / len(loop)])
            _to   = marginleft + ll("FELD" + loop[count])
            while c < steps:

                # line
                direction = 1 if (_from < _to) else -1
                _step = _to + (int((float(abs(_from - _to)) / steps) * (steps - c))) * direction
                graphics.DrawLine(canvas, marginleft + ll("FELD"), margintop + 1, _step, margintop + 1, white)

                # dot
                canvas.SetPixel(_step, margintop - 1,255,255,255)

                # feld
                graphics.DrawText(canvas, font, marginleft, margintop, white, "FELD")

                # man
                y_man = margintop - int((float(5) / steps) * (steps - c))
                graphics.DrawText(canvas, font, marginleft + ll("FELD"), y_man, white, loop[count])

                c += 1
                time.sleep(0.01)
                canvas = self.matrix.SwapOnVSync(canvas)
                canvas.Clear()

            time.sleep(1.5)

            count += 1
            count = count % len(loop)

# Main function
if __name__ == "__main__":
    if args.simple_loader:
        feldman = Feld({"api": False})
    elif args.call_api:
        feldman = Feld({"api": True})
    if (not feldman.process()):
        feldman.print_help()

# font

#####################

# SetPixel
# canvas.SetPixel(x,y,r,g,b)

# DrawLine
# graphics.DrawLine(canvas, x0, y0, x1, y1, graphics.Color(255, 0, 0))

# DrawCircle
# graphics.DrawCircle(canvas, cx, cy, r, graphics.Color(255, 0, 0))

# DrawText
# graphics.DrawText(canvas, font, 2, 10, blue, "Text")

# Fill
# self.matrix.Fill(c, 0, 0)
