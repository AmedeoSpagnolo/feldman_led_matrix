from rgbmatrix import graphics

FONT = graphics.Font()
MAIN_COLOR = graphics.Color(255,255,255)

MARGIN_LEFT = 0
MARGIN_TOP = 14

FELD_LOOP = [
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


# FONT.LoadFont("libs/fonts/4x6.bdf")
FONT.LoadFont("libs/newfont/converted_14.bdf")

ANIMATION_TIME = 10
SHIFT = 5

PREFIX = "FELD"
