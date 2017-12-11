#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
import time

class Feld(SampleBase):
    def __init__(self, *args, **kwargs):
        super(Feld, self).__init__(*args, **kwargs)

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

    def run(self):
        canvas = self.matrix.CreateFrameCanvas()

        red     = graphics.Color(255, 0, 0)
        green   = graphics.Color(0, 255, 0)
        blue    = graphics.Color(0, 0, 255)
        white   = graphics.Color(255,255,255)
        font    = graphics.Font()
        font.LoadFont("../fonts/4x6.bdf")

        # position
        # pos = offscreen_canvas.width

        # brightness
        max_brightness = self.matrix.brightness

        loop = [
          "man",
          "design",
          "branding",
          "advertising",
          "typography",
          "photography",
          "illustration",
          "editorial",
          "video",
          "print",
          "web"
        ]

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

                # line and dot
                if _from < _to:
                    _step = _to - int((float(abs(_from - _to)) / steps) * (steps - c))
                else:
                    _step = _to + int((float(abs(_from - _to)) / steps) * (steps - c))
                graphics.DrawLine(canvas, marginleft + ll("FELD"), margintop + 1, _step, margintop + 1, white)
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
    feldman = Feld()
    if (not feldman.process()):
        feldman.print_help()

# font
# connessione server
