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
        op = {
            'x': MARGIN_LEFT,
            'y': MARGIN_TOP,
            'font': FONT,
            'anim': True,
            'anim_time': ANIMATION_TIME,
            'outline': True,
            'prefix': "FELD",
            'color': MAIN_COLOR}
        op.update(opt)
        count = op['anim_time'] if op['anim'] else 1
        pref_shift = self.ll(op['prefix']) if op['prefix'] else 0
        delta_words = self.word - self.prev
        while count > 0:
            self.offscreen_canvas.Clear()
            anim_shift = int(float(SHIFT) / op['anim_time'] * count)
            # anim_line = int((float(abs(prev_word_len - word_length)) / ANIM_TIME) * (ANIM_TIME - c))
            graphics.DrawText(self.offscreen_canvas, op['font'], pref_shift + op['x'], op['y'] - anim_shift, op['color'], word + '.')
            if op['prefix']:
                graphics.DrawText(self.offscreen_canvas, op['font'], op['x'], op['y'], op['color'], op['prefix'])
            if op['outline']:
                graphics.DrawLine(self.offscreen_canvas, pref_shift + op['x'], op['y'] + 1, pref_shift+self.ll(word), op['y'] + 1, op["color"])
            self.offscreen_canvas = self.canvas.SwapOnVSync(self.offscreen_canvas)
            time.sleep(0.01)
            count -= 1

    def run(self):
        print "[*] starting..."
        print "Press CTRL-C to stop"

        # [*] MODE
        # single word
        if self.args.word:
            print "[*] MODE: Single word"
            self.word = self.args.word[0]
            print "data: %s" % (self.word)
            while True:
                self.drawtext(self.word)
                time.sleep(2)

        # [*] MODE
        # Loader
        if self.args.loader:
            print "[*] MODE: Loader"
            count = 0
            while True:
                self.prev = self.word
                self.word = FELD_LOOP[count]
                print "data: %s" % (self.word)
                self.drawtext(self.word)
                count = (1 + count) % len(FELD_LOOP)
                time.sleep(2)

        # [*] MODE
        # Socket
        if self.args.socket:
            print "[*] MODE: Socket"
            sio = socketio.Server()
            app = Flask(__name__)

            @sio.on('news')
            def message(sid, data):
                print "data: %s" % data
                sio.emit('reply', "received: %s" % data)
                if isblacklisted(data):
                    self.prev = self.word
                    self.word = data
                    self.drawtext(self.word)

            # wrap Flask application with engineio's middleware
            app = socketio.Middleware(sio, app)

            # deploy as an eventlet WSGI server
            eventlet.wsgi.server(eventlet.listen(('', int(self.args.port[0]))), app)

# Main function
if __name__ == "__main__":
    feldman = Feld()
