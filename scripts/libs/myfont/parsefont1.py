import re
import sys
import json

def read_text(file_name):
    with open(file_name, "r") as f:
        return f.read()

def ord2char(arr):
    if not isinstance(arr, list): arr = [arr]
    return [unichr(i) for i in arr]

def hex2bin(arr, zeros = 30):
    if not isinstance(arr, list): arr = [arr]
    return [bin(int(i, 16))[2:].zfill(zeros) for i in arr]

def char2ord(string):
    return [ord(i) for i in list(string)]

text = read_text("converted_9.bdf")

text = re.sub(r'\n', '{{}}', text)
text = re.sub(r'ENDCHAR{{}}', 'ENDCHAR\n', text)
# matches = re.finditer(r'ENCODING\s(\d+)|BITMAP(.*)ENDCHAR', text, re.MULTILINE)
matches = re.finditer(r"ENCODING\s(\d+)|BITMAP(.*)ENDCHAR|DWIDTH\s(\d+)", text, re.MULTILINE)
output = {}
current = "0"
count = 2
for matchNum, match in enumerate(matches):
    # mychar,tmp = match.groups()
    # tmp,content = match.groups()
    tmp = match.groups()[2-count]

    # len
    if (count == 0):
        output["_" + current]["len"] = int(tmp)

    # val
    elif (count == 1):
        output["_" + current]["val"] = re.sub(r'{{}}', '\n', tmp)

    # ord
    else:
        current = ord2char(int(tmp))[0]
        output["_" + current] = {"ord": tmp, "char": current}

    count += 1
    count = count % 3

def printall():
    for key, value in output.iteritems():
        try:
            print "%s: %s" % (key[1:], value["ord"])
            print "\n".join(hex2bin(value["val"].splitlines()[1:],value["len"]))
        except:
            pass

def printchar(c):
    key = char2ord(c)
    value = output["_"+c]
    # print value
    print "%s: %s" % (c, value["ord"])
    print "\n".join(hex2bin(value["val"].splitlines()[1:],value["len"]))

# printall()
printchar("C")
printchar("D")
printchar("E")
printchar("G")
