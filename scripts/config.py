import json
from rgbmatrix import graphics

FELD_LOOP = json.load(open('assets/datasets/feldloop.json'))
ANIM_TIME = 15

FONT = graphics.Font()
MAIN_COLOR = graphics.Color(255,255,255)
BRIGHTNESS = 50

MARGIN_TOP = 0
MARGIN_LEFT = 0
