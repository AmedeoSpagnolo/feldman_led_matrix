import re
import sys

def read_text(file_name):
    with open(file_name, "r") as f:
        return f.read()

text = read_text("converted_9.bdf")
# # regex = r'STARTCHAR(.*)ENDCHAR'
# # regex = "(?<=STARTCHAR)(.*|.*\n)(?=BBX)"
# # matches = re.search(regex, text, re.MULTILINE)
# matches = re.findall(r'STARTCHAR(.*)ENDCHAR', text, flags=re.DOTALL|)
# # regex = re.compile(r'(?<=STARTCHAR)(.*)(?=ENDCHAR)', re.DOTALL)
# # my_chars = regex.findall(text)
#
# print len(matches)
# # print matches[0]
#
# r'STARTCHAR(.*)ENDCHAR'



# rx_sequence=re.compile(r'STARTCHAR(.*)ENDCHAR',re.MULTILINE)
# rx_blanks=re.compile(r"\W+")
#
# print rx_sequence.finditer(text)



# rx_sequence=re.compile(r"^(.+?)\n\n((?:[A-Z]+\n)+)",re.MULTILINE)
# rx_blanks=re.compile(r"\W+") # to remove blanks and newlines
text1="""Some varying text1

AAABBBBBBCCCCCCDDDDDDD
EEEEEEEFFFFFFFFGGGGGGG
HHHHHHIIIIIJJJJJJJKKKK

Some varying text 2

LLLLLMMMMMMNNNNNNNOOOO
PPPPPPPQQQQQQRRRRRRSSS
TTTTTUUUUUVVVVVVWWWWWW
"""

text = re.sub(r'\n', "{{{space}}}" , text)
text = re.sub(r'{{{space}}}ENDCHAR', "\nENDCHAR" , text)
text = re.sub(r'STARTCHAR\s([\w]+)(.*)+', $1, text)

print text
regex = r'STARTCHAR(.*)ENDCHAR'
# matches = re.findall(regex, text, flags=re.)
# print len(matches)

# print re.sub(r'\t', "\n" , text)

# for match in rx_sequence.finditer(text):
#     title, sequence = match.groups()
#     title = title.strip()
#     sequence = rx_blanks.sub("",sequence)
#     print "Title:",title
#     print "Sequence:",sequence
#     print
