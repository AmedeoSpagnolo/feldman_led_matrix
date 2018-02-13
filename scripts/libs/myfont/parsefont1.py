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

text = read_text("converted_9.bdf")

text = re.sub(r'\n', '{{}}', text)
text = re.sub(r'ENDCHAR{{}}', 'ENDCHAR\n', text)
matches = re.finditer(r'ENCODING\s(\d+)|BITMAP(.*)ENDCHAR', text, re.MULTILINE)
output = {}
current = ""
for matchNum, match in enumerate(matches):
    mychar,tmp = match.groups()
    tmp,content = match.groups()
    if mychar:
        current = ord2char(int(mychar))[0]
        output["_" + current] = {"ord": mychar, "c": current}
    if content:
        output["_" + current]["values"] = re.sub(r'{{}}', '\n', content)

    # print ord2char(int(match.group(1)))
    # output[ord2char(match.group(1))] = "asd"
# print json.dumps(output, indent = 4)

for key, value in output.iteritems():
    try:
        print key
        print "\n".join(hex2bin((value["values"]).splitlines()[1:]))
    except:
        pass
    # print v
