#!/usr/bin/env python

import sys
import os
sys.path.append(sys.path[0])
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

from rgbmatrix import graphics, RGBMatrixOptions, RGBMatrix

from libs.blacklist import *
from libs.config import *

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
            "--prefix",
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

    def ll(self, string):
        return sum([FONT.CharacterWidth(ord(c)) for c in string])

    def drawtext(self, word, opt = {}):
        self.prev = self.word
        self.word = word
        print "prev: " + str(self.prev)
        print "word: " + str(self.word)
        op = {
            'x': MARGIN_LEFT,
            'y': MARGIN_TOP,
            'font': FONT,
            'anim': True,
            'anim_time': ANIMATION_TIME,
            'outline': True,
            'prefix': "FELD",
            'suffix': ".",
            'color': MAIN_COLOR}
        op.update(opt)
        count = op['anim_time'] if op['anim'] else 1
        pref_shift = self.ll(op['prefix']) if op['prefix'] else 0
        delta_words = self.ll(self.word) - self.ll(self.prev)
        while count > 0:
            self.offscreen_canvas.Clear()
            anim_y_shift = int(float(SHIFT) / op['anim_time'] * count)
            anim_ln_line = int(float(delta_words) / op['anim_time'] * count)
            _x = pref_shift + op['x']
            _y = op['y'] - anim_y_shift
            graphics.DrawText(self.offscreen_canvas, op['font'], _x, _y, op['color'], word + op['suffix'])
            if op['prefix']:
                graphics.DrawText(self.offscreen_canvas, op['font'], op['x'], op['y'], op['color'], op['prefix'])
            if op['outline']:
                __x1 = _x
                __x2 = pref_shift + self.ll(word) + 2 - anim_ln_line
                __y = op['y'] + 1
                graphics.DrawLine(self.offscreen_canvas, __x1, __y, __x2, __y, op["color"])
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
            print "data: %s" % (FELD_LOOP[count])
            self.drawtext(FELD_LOOP[count])
            count = (1 + count) % len(FELD_LOOP)
            time.sleep(2)

    def mode_socket(self):
        print "[*] MODE: Socket"
        sio = socketio.Server()
        app = Flask(__name__)
        self.drawtext("", {'suffix': '', 'anim': False, 'outline': False})

        @sio.on('news')
        def message(sid, data):
            print "data: %s" % data
            sio.emit('reply', "received: %s" % data)
            if not isblacklisted(data):
                self.drawtext(data)
                # todo : animation slow
            else:
                print dir(sio)
                print "received banned word: %s from %s" % (data, sid)

        # wrap Flask application with engineio's middleware
        app = socketio.Middleware(sio, app)

        # deploy as an eventlet WSGI server
        eventlet.wsgi.server(eventlet.listen(('', int(self.args.port[0]))), app)

    def run(self):
        print "[*] starting..."
        print "Press CTRL-C to stop"

        # [*] MODE: single word
        if self.args.word:
            self.mode_single_word()

        # [*] MODE: Loader
        if self.args.loader:
            self.mode_loader()

        # [*] MODE: Socket
        if self.args.socket:
            self.mode_socket()

# Main function
if __name__ == "__main__":
    feldman = Feld()
