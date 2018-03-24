import re
import sys
import json

def ord2char(arr):
    if not isinstance(arr, list): arr = [arr]
    return [unichr(i) for i in arr]

def hex2bin(arr, zeros = 30):
    if not isinstance(arr, list): arr = [arr]
    return [bin(int(i, 16))[2:].zfill(zeros) for i in arr]

def bin2hex(arr, zeros = 4):
    if not isinstance(arr, list): arr = [arr]
    return [hex(int(i, 2))[2:].zfill(zeros).upper() for i in arr]

def multilinebin2hex(str):
    print str + "\n"
    return "\n".join(bin2hex(str.splitlines()))

newdesign = """000000110011110001111100000000
000000110111111011111110000000
000000111000011110000111000000
000000110000001100000011000000
000000110000001100000011000000
000000110000001100000011000000
000000110000001100000011000000
000000110000001100000011000000
000000110000001100000011000000
000000110000001100000011000000
000000110000001100000011000000
000000110000001100000011000000"""

print multilinebin2hex(newdesign)
print ""
