from rgbmatrix import graphics, RGBMatrixOptions, RGBMatrix
from config import *

FONT.LoadFont("fonts/4x6.bdf")


def canvas_init(arg):
    options = RGBMatrixOptions()
    if arg.led_gpio_mapping != None:
      options.hardware_mapping = arg.led_gpio_mapping
    options.rows = arg.led_rows
    options.chain_length = arg.led_chain
    options.parallel = arg.led_parallel
    options.pwm_bits = arg.led_pwm_bits
    options.brightness = arg.led_brightness
    options.pwm_lsb_nanoseconds = arg.led_pwm_lsb_nanoseconds
    options.led_rgb_sequence = arg.led_rgb_sequence
    if arg.led_show_refresh:
      options.show_refresh_rate = 1
    if arg.led_slowdown_gpio != None:
        options.gpio_slowdown = arg.led_slowdown_gpio
    if arg.led_no_hardware_pulse:
      options.disable_hardware_pulsing = True
    return RGBMatrix(options = options)

def print_line(canvas):
    while True:
        l = {
            "x0": 10, "y0": 3,
            "x1": 20, "y1": 3,
            "color": MAIN_COLOR}
        graphics.DrawLine(canvas, l["x0"], l["y0"], l["x1"], l["y1"], l["color"])

def print_word(word, canvas, seconds):
    count = 0
    while count < seconds * 50000:
        canvas.Clear()
        m = {
            "text":     word,
            "x0":       1,
            "y0":       HEIGHT - 2,
            "color":    MAIN_COLOR}
        m1 = {
            "text":     "word",
            "x0":       2,
            "y0":       5,
            "color":    MAIN_COLOR}
        graphics.DrawText(canvas, FONT, m["x0"], m["y0"], m["color"], m["text"])
        count += 1




#
# def print_word(self, word, canvas, prefix, prev_word):
#
#     def ll(string):
#         return sum([font.CharacterWidth(ord(c)) for c in string])
#
#     c   = 0
#     font    = FONT
#
#     margin_bottom   = 2
#     margin_top      = self.matrix.height - 8
#     word_length     = margin_bottom + ll("FELD" + word)
#     prev_word_len   = margin_bottom + ll("FELD" + self.prev_word)
#     sign            = 1 if (prev_word_len < word_length) else -1
#
#     self.matrix.brightness = BRIGHTNESS
#     font.LoadFont("assets/fonts/4x6.bdf")
#
#     while (c < ANIM_TIME):
#         canvas.Clear()
#
#         # line
#         l = {
#             "x0": margin_bottom + ll("FELD"),
#             "y0": margin_top + 1,
#             "x1": word_length + (int((float(abs(prev_word_len - word_length)) / ANIM_TIME) * (ANIM_TIME - c))) * sign,
#             "y1": margin_top + 1,
#             "color": graphics.Color(255,255,255)
#         }
#         graphics.DrawLine(canvas, l["x0"], l["y0"], l["x1"], l["y1"], l["color"])
#
#         # dot
#         d = {
#             "x": l["x1"],
#             "y": margin_top - 1,
#             "col": {"r": 255, "g": 255, "b": 255}
#         }
#         canvas.SetPixel(d["x"], d["y"], d["col"]["r"], d["col"]["g"], d["col"]["b"])
#
#         # feld
#         f = {
#             "x0": margin_bottom,
#             "y0": margin_top,
#             "color": graphics.Color(255,255,255)
#         }
#         graphics.DrawText(canvas, font, f["x0"], f["y0"], f["color"], "FELD")
#
#         # man
#         m = {
#             "x0": margin_bottom + ll("FELD"),
#             "y0": margin_top - int((float(5) / ANIM_TIME) * (ANIM_TIME - c)),
#             "color": graphics.Color(255,255,255)
#         }
#         graphics.DrawText(canvas, font, m["x0"], m["y0"], m["color"], word)
#
#         c += 1
#         time.sleep(0.01)
#
#         canvas = self.matrix.SwapOnVSync(canvas)
#
#     self.prev_word = word
