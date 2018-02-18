from rgbmatrix import graphics

FONT_MAIN = graphics.Font()
FONT_MAIN.LoadFont("libs/myfont/weights/font_16.bdf")

FONT_BOLD = graphics.Font()
FONT_BOLD.LoadFont("libs/myfont/weights/font_16_b.bdf")

MAIN_COLOR = graphics.Color(255,255,255)

MARGIN_LEFT = 0
MARGIN_TOP = 20

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

ANIMATION_TIME = 10
YSHIFT = 5

PREFIX = "Feld"
