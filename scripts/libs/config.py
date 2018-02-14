from rgbmatrix import graphics

FONT_MAIN = graphics.Font()
FONT_MAIN.LoadFont("libs/myfont/font_book.bdf")

FONT_BOLD = graphics.Font()
FONT_BOLD.LoadFont("libs/myfont/font_bold.bdf")

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

ANIMATION_TIME = 10
SHIFT = 5

PREFIX = "Feld"

# libs/fonts/4x6.bdf
# libs/myfont/converted_9.bdf
# libs/myfont/converted_11_b.bdf
