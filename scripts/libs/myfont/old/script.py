F = ["FF","FF","C0","C0","C0","C0","FF","FF","C0","C0","C0","C0","C0","C0"]
e = ["3D80","7F80","C380","C180","C180","C180","C180","6380","7F80","0980","C180","C300","7F00","3E00"]
M = ["BCF0","EFB8","C718","8218","8218","8218","8218","8218","8218","8218"]
m_bin = ["1101111001111100", "1111011111101110", "1110001111000110", "1100000110000110", "1100000110000110", "1100000110000110", "1100000110000110", "1100000110000110", "1100000110000110", "1100000110000110"]
m_bin1 = """1101111001111100
1111011111101110
1110001111000110
1100000110000110
1100000110000110
1100000110000110
1100000110000110
1100000110000110
1100000110000110
1100000110000110"""

G = """0F80
3FE0
7070
6038
C010
C000
C000
C3F8
C3F8
C018
6038
7078
3FD8
0F98"""

G_bin = """000000000000000000111110000000
000000000000000011111111100000
000000000000000111000001110000
000000000000000110000000111000
000000000000001100000000010000
000000000000001100000000000000
000000000000001100000000000000
000000000000001100001111111000
000000000000001100001111111000
000000000000001100000000011000
000000000000000110000000111000
000000000000000111000001111000
000000000000000011111111011000
000000000000000000111110011000"""

def char2ord(string):
    return [ord(i) for i in list(string)]

def ord2char(arr):
    if not isinstance(arr, list): arr = [arr]
    return [unichr(i) for i in arr]

def hex2bin(arr, zeros = 30):
    if not isinstance(arr, list): arr = [arr]
    return [bin(int(i, 16))[2:].zfill(zeros) for i in arr]

def bin2hex(arr, zeros = 4):
    if not isinstance(arr, list): arr = [arr]
    return [hex(int(i,2))[2:].zfill(zeros) for i in arr]

def print_help():
    print "char2ord('A'): %s" % (char2ord('A'))
    print "char2ord('Aa'): %s" % (char2ord('Aa'))
    print "ord2char(65): %s" % (ord2char(65))
    print "ord2char([65, 97]): %s" % (ord2char([65, 97]))
    print "hex2bin('FA'): %s" % hex2bin('FA')
    print "bin2hex('11111010'): %s" % bin2hex('11111010')
    print "m_bin:"
    show (m_bin)
    print "bin2hex(m_bin):"
    show (bin2hex(m_bin))
    print "m_bin1.splitlines():"
    show (m_bin1.splitlines())
    print "bin2hex(m_bin1.splitlines()):"
    show (bin2hex(m_bin1.splitlines()))
    print char2ord("G")
    show(hex2bin(G.splitlines()))
    print G
    print ""
    show(bin2hex(G_bin.splitlines()))

def show(arr):
    for i in arr:
        print i

print_help()
