# #!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
import time
import json

class Feld(SampleBase):
    def __init__(self, *args, **kwargs):
        super(Feld, self).__init__(*args, **kwargs)
        print "opt"

    def run(self):
        canvas = self.matrix.CreateFrameCanvas()

        # assets
        red     = graphics.Color(255, 0, 0)
        green   = graphics.Color(0, 255, 0)
        blue    = graphics.Color(0, 0, 255)
        white   = graphics.Color(255,255,255)
        font    = graphics.Font()
        loop    = json.load(open('assets/datasets/feldloop.json'))
        font.LoadFont("assets/fonts/4x6.bdf")
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
