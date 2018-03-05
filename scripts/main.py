#!/usr/bin/env python
import sys
import os
sys.path.append(sys.path[0])
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

from rgbmatrix import graphics, RGBMatrixOptions, RGBMatrix
from libs.blacklist import *
from libs.timer import *

import math
import argparse
import time
import requests
import threading
import random
import socketio
import eventlet
import eventlet.wsgi

from flask import Flask, render_template

class Feld():
    def __init__(self, *args, **kwargs):
        self.parser = argparse.ArgumentParser()

        self.parser.add_argument(
            "-s", "--socket",
            action="store_true",
            help="get words from socket")
        self.parser.add_argument(
            '--port',
            nargs=1,
            default=False,
            required=False,
            type=int,
            help="with -s/--socket specify port for connection")
        self.parser.add_argument(
            "--suffx",
            nargs=1,
            default=False,
            required=False,
            help="add prefix",
            type=str)
        self.parser.add_argument(
            "--loader",
            action="store_true",
            help="print loader words")
        self.parser.add_argument(
            '--test_font_bold',
            nargs=1,
            default=False,
            required=False,
            help="write a word",
            type=str)
        self.parser.add_argument(
            '--test_font_book',
            nargs=1,
            default=False,
            required=False,
            help="write a word",
            type=str)
        self.parser.add_argument(
            '--word',
            nargs=1,
            default=False,
            required=False,
            help="write a word",
            type=str)
        self.parser.add_argument(
            "-r", "--led-rows",
            action="store",
            help="Display rows. 16 for 16x32, 32 for 32x32. Default: 32",
            default=32,
            type=int)
        self.parser.add_argument(
            "-c", "--led-chain",
            action="store",
            help="Daisy-chained boards. Default: 1.",
            default=1,
            type=int)
        self.parser.add_argument(
            "-P", "--led-parallel",
            action="store",
            help="For Plus-models or RPi2: parallel chains. 1..3. Default: 1",
            default=1,
            type=int)
        self.parser.add_argument(
            "-p", "--led-pwm-bits",
            action="store",
            help="Bits used for PWM. Something between 1..11. Default: 11",
            default=11,
            type=int)
        self.parser.add_argument(
            "-b", "--led-brightness",
            action="store",
            help="Sets brightness level. Default: 100. Range: 1..100",
            default=100,
            type=int)
        self.parser.add_argument(
            "-m", "--led-gpio-mapping",
            help="Hardware Mapping: regular, adafruit-hat, adafruit-hat-pwm" ,
            choices=['regular', 'adafruit-hat', 'adafruit-hat-pwm'],
            type=str)
        self.parser.add_argument(
            "--led-scan-mode",
            action="store",
            help="Progressive or interlaced scan. 0 Progressive, 1 Interlaced (default)",
            default=1,
            choices=range(2),
            type=int)
        self.parser.add_argument(
            "--led-pwm-lsb-nanoseconds",
            action="store",
            help="Base time-unit for the on-time in the lowest significant bit in nanoseconds. Default: 130",
            default=130,
            type=int)
        self.parser.add_argument(
            "--led-show-refresh",
            action="store_true",
            help="Shows the current refresh rate of the LED panel")
        self.parser.add_argument(
            "--led-slowdown-gpio",
            action="store",
            help="Slow down writing to GPIO. Range: 1..3. Default: 1",
            choices=range(3),
            type=int)
        self.parser.add_argument(
            "--led-no-hardware-pulse",
            action="store",
            help="Don't use hardware pin-pulse generation")
        self.parser.add_argument(
            "--led-rgb-sequence",
            action="store",
            help="Switch if your matrix has led colors swapped. Default: RGB",
            default="RGB",
            type=str)
        self.parser.add_argument(
            '--margin_left',
            nargs=1,
            default=False,
            required=False,
            help="set margin left",
            type=int)
        self.parser.add_argument(
            '--margin_top',
            nargs=1,
            default=False,
            required=False,
            help="set margin top",
            type=int)
        self.parser.add_argument(
            '--space_after_prefix',
            nargs=1,
            default=False,
            required=False,
            help="set space after prefix",
            type=int)
        self.parser.add_argument(
            '--space_before_suffix',
            nargs=1,
            default=False,
            required=False,
            help="set space after prefix",
            type=int)
        self.parser.add_argument(
            '--animation_time',
            nargs=1,
            default=False,
            required=False,
            help="set animation time, default 10",
            type=int)
        self.parser.add_argument(
            '--yshift',
            nargs=1,
            default=False,
            required=False,
            help="set animation y shift",
            type=int)
        self.parser.add_argument(
            '--prefx',
            nargs=1,
            default=False,
            required=False,
            help="set prefix",
            type=str)
        self.parser.add_argument(
            '--font_main',
            nargs=1,
            default=False,
            required=False,
            help="font book height in pixel",
            type=int)
        self.parser.add_argument(
            '--font_bold',
            nargs=1,
            default=False,
            required=False,
            help="font bold height in pixel",
            type=int)
        self.args = self.parser.parse_args()

        self.canvas = self.canvas_init(self.args)
        self.offscreen_canvas = self.canvas.CreateFrameCanvas()

        self.word = ''
        self.prev = ''

        try:
            self.run()
        except KeyboardInterrupt:
            print("Exiting\n")
            sys.exit(0)

    # todo
    def canvas_init(self, arg):
        options = RGBMatrixOptions()
        options.rows = arg.led_rows
        fontsize_book = int(arg.font_main[0]) if arg.font_main else 16
        fontsize_bold = int(arg.font_bold[0]) if arg.font_bold else 16
        self.FELD_LOOP = [
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
            "web"]
        self.ANIMATION_TIME = arg.animation_time[0] if arg.animation_time else 10
        self.YSHIFT = arg.yshift[0] if arg.yshift else 5
        self.PREFIX = arg.prefx[0] if arg.prefx else "Feld"
        self.SUFFIX = arg.suffx[0] if arg.suffx else ""
        self.MAIN_COLOR = graphics.Color(255,255,255)
        self.MARGIN_LEFT = arg.margin_left[0] if arg.margin_left else 0
        self.MARGIN_TOP = arg.margin_top[0] if arg.margin_top else (options.rows + fontsize_bold)/2
        self.FONT_MAIN = graphics.Font()
        self.FONT_MAIN.LoadFont("libs/myfont/weights/font_" + str(fontsize_book) + "_book.bdf")
        self.FONT_BOLD = graphics.Font()
        self.FONT_BOLD.LoadFont("libs/myfont/weights/font_" + str(fontsize_bold) + "_bold.bdf")
        self.SPACE_AFTER_PREFIX = arg.space_after_prefix[0] if arg.space_after_prefix else 0
        self.SPACE_BEFORE_SUFFIX = arg.space_before_suffix[0] if arg.space_before_suffix else 0
        if arg.led_gpio_mapping != None:
          options.hardware_mapping = arg.led_gpio_mapping
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

    def ll(self, string, font, spacing = 3):
        spaces = len(string) * spacing
        return sum([font.CharacterWidth(ord(c)) for c in string]) + spaces

    def drawtext(self, word = random.choice(self.FELD_LOOP), opt = {}):
        self.prev = self.word
        self.word = word
        op = {
            'ml': self.MARGIN_LEFT,
            'mt': self.MARGIN_TOP,
            'dot': True,
            'anim': True,
            'outline': True,
            'color': self.MAIN_COLOR,
            'prefix': self.PREFIX,
            'suffix': self.SUFFIX,
            'anim_time': self.ANIMATION_TIME,
            'font_book': self.FONT_MAIN,
            'font_bold': self.FONT_BOLD,}
        op.update(opt)

        delta_words = self.ll(self.word, op['font_book']) - self.ll(self.prev, op['font_book'])
        prefix_length = self.ll(op['prefix'], op['font_bold'], 1) if op['prefix'] else 0
        word_length = self.ll(word, op['font_book'], 1)

        count = op['anim_time'] if op['anim'] else 1
        while count > 0:
            self.offscreen_canvas.Clear()

            anim_y_shift = int(float(self.YSHIFT) / op['anim_time'] * count)
            anim_x_shift = int(float(delta_words) / op['anim_time'] * (count - 1))

            # anim_y_shift = int(math.pow(float(self.YSHIFT),-1) / math.pow(op['anim_time'],-1) * count)
            # anim_x_shift = int(math.pow(float(delta_words),-1) / math.pow(op['anim_time'],-1) * (count - 1))

            baseline = op['mt'] # y
            X0 = op['ml'] # prefix x value
            X1 = op['ml'] + prefix_length + self.SPACE_AFTER_PREFIX # word x value
            X2 = X1 + self.ll(word, op['font_book']) + self.SPACE_BEFORE_SUFFIX # dot x value

            # [-- DRAW --]: prefix
            if op['prefix']:
                graphics.DrawText(self.offscreen_canvas, op['font_bold'], X0, baseline, op['color'], op['prefix'])

            # [-- DRAW --]: word
            graphics.DrawText(self.offscreen_canvas, op['font_book'], X1, baseline - anim_y_shift, op['color'], word)

            # [-- DRAW --]: outline
            if op['outline']:
                graphics.DrawLine(self.offscreen_canvas, X1, baseline + 2, X2 + 1 - anim_x_shift, baseline + 2, op["color"])
                graphics.DrawLine(self.offscreen_canvas, X1, baseline + 3, X2 + 1 - anim_x_shift, baseline + 3, op["color"])

            # [-- DRAW --]: dot
            if op['dot']:
                graphics.DrawLine(self.offscreen_canvas, X2 + 1 - anim_x_shift, baseline - 2, X2 - anim_x_shift, baseline - 2, op["color"])
                graphics.DrawLine(self.offscreen_canvas, X2 + 1 - anim_x_shift, baseline - 1, X2 - anim_x_shift, baseline - 1, op["color"])

            # [-- DRAW --]: suffix
            if op['suffix']:
                graphics.DrawText(self.offscreen_canvas, op['font_bold'], X2 + 3 - anim_x_shift, baseline, op['color'], op['suffix'])

            self.offscreen_canvas = self.canvas.SwapOnVSync(self.offscreen_canvas)
            time.sleep(0.01)
            count -= 1

    def mode_single_word(self):
        print "[*] MODE: Single word"
        print "data: %s" % (self.args.word[0])
        while True:
            self.drawtext(self.args.word[0], {'anim': False})
            time.sleep(2)

    def mode_loader(self):
        print "[*] MODE: Loader"
        count = 0
        while True:
            print "data: %s" % (self.FELD_LOOP[count])
            self.drawtext(self.FELD_LOOP[count])
            count = (1 + count) % len(self.FELD_LOOP)
            time.sleep(2)

    def mode_socket(self):
        print "[*] MODE: Socket"
        sio = socketio.Server()
        app = Flask(__name__)
        self.drawtext("", {'suffix': '', 'anim': False, 'outline': False})
        t = RepeatingTimer(5, self.drawtext)
        t.start()

        @sio.on('news')
        def message(sid, data):
            t.cancel()
            t.start()
            print "data: %s" % data
            sio.emit('reply', "received: %s" % data)
            if not isblacklisted(data):
                time.sleep(0.5)
                self.drawtext(data)
            else:
                print "received banned word: %s from %s" % (data, sid)

        # wrap Flask application with engineio's middleware
        app = socketio.Middleware(sio, app)

        # deploy as an eventlet WSGI server
        eventlet.wsgi.server(eventlet.listen(('', int(self.args.port[0]))), app)

    def mode_test_font_bold(self):
        print "[*] MODE: Test Font Bold"
        print "data: %s" % (self.args.test_font_bold[0])
        while True:
            self.drawtext(self.args.test_font_bold[0], {
                'prefix': '', 'suffix': '',
                'font_book': self.FONT_BOLD,
                'anim': False, 'outline': False})
            time.sleep(2)

    def mode_test_font_book(self):
        print "[*] MODE: Test Font Book"
        print "data: %s" % (self.args.test_font_book[0])
        while True:
            self.drawtext(self.args.test_font_book[0], {
                'prefix': '', 'suffix': '',
                'anim': False, 'outline': False})
            time.sleep(2)

    def run(self):
        print "[*] starting..."
        print "Press CTRL-C to stop"

        # [*] MODE: Single Word
        if self.args.word:
            self.mode_single_word()

        # [*] MODE: Loader
        if self.args.loader:
            self.mode_loader()

        # [*] MODE: Socket
        if self.args.socket:
            self.mode_socket()

        # [*] MODE: Test Font Bold
        if self.args.test_font_bold:
            self.mode_test_font_bold()

        # [*] MODE: Test Font Book
        if self.args.test_font_book:
            self.mode_test_font_book()

# Main function
if __name__ == "__main__":
    feldman = Feld()
