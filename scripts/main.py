#!/usr/bin/env python

import sys
import os
sys.path.append(sys.path[0])
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

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

        try:
            self.run()
        except KeyboardInterrupt:
            print("Exiting\n")
            sys.exit(0)

    # todo
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

    def run(self):

<<<<<<< HEAD
        c = self.canvas.CreateFrameCanvas()

        # start
        w = self.args.word[0] if self.args.word else "start"
        # print_word(w, self.matrix.CreateFrameCanvas(), self.args.prefix, self.prev_word)
        print "[*] starting..."
        print "Press CTRL-C to stop sample"
        print "data: %s\n" % (w)
        self.printword(w, 15)
=======
        print "[*] starting..."
        print "Press CTRL-C to stop"

        # [*] MODE
        # single word
        if self.args.word:
            w = self.args.word[0]
            print "[*] MODE: single word"
            print "data: %s" % (w)
            while True:
                w = FELD_LOOP[count]
                offscreen_canvas.Clear()
                graphics.DrawText(offscreen_canvas, FONT, 10, 10, MAIN_COLOR, w)
                time.sleep(0.05)
                offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
>>>>>>> 81b664d5849051e9ca1d24d8515182ebf5299f4b

        # [*] MODE
        # only loader
        if self.args.loader:
            print "[*] MODE: only loader"
            count = 0
            while True:
                w = FELD_LOOP[count]
                print "data: %s" % (w)
                offscreen_canvas.Clear()
                graphics.DrawText(offscreen_canvas, FONT, 10, 10, MAIN_COLOR, w)
                time.sleep(0.05)
                count = (1 + count) % len(FELD_LOOP)
                offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

        # [*] MODE
        # only socket
        if self.args.socket:
            print "[*] MODE: only socket"
            sio = socketio.Server()
            app = Flask(__name__)

            @sio.on('news')
            def message(sid, data):
                print "data: %s" % data
                sio.emit('reply', "received: %s" % data)
                # print_word(data, self.matrix.CreateFrameCanvas(), self.args.prefix, self.prev_word)

            # wrap Flask application with engineio's middleware
            app = socketio.Middleware(sio, app)

            # deploy as an eventlet WSGI server
            eventlet.wsgi.server(eventlet.listen(('', int(self.args.port[0]))), app)


# Main function
if __name__ == "__main__":
    feldman = Feld()
