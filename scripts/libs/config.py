from rgbmatrix import graphics

FONT = graphics.Font()
MAIN_COLOR = graphics.Color(255,255,255)

MARGIN_LEFT = 1
MARGIN_TOP = 16

print dir(FONT)
print FONT.height
print FONT.baseline

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
FONT.LoadFont("libs/fonts/converted_5.bdf")

ANIMATION_TIME = 10
SHIFT = 5

PREFIX = "feld"
