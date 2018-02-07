import json
import os
import sys

wordlist = json.load(open(os.path.dirname(__file__) + '/blacklist.json'))

def isblacklisted(sentence):
    return not all([i not in wordlist for i in sentence.split()])

def list_blacklist():
    return wordlist
