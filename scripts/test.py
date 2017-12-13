import json
import random
import requests
import threading

blacklist   = json.load(open('blacklist.json'))
feldloop    = json.load(open('feldloop.json'))
names       = json.load(open('names.json'))

def isblacklisted(sentence):
    if (any([ (i in " ".join(blacklist)) for i in sentence.split()])):
        return True
    else:
        return False

def get_word_from_list(arr):
    return arr[random.randint(0,len(arr)-1)]

def get_word_from_api(url):
    try:
        r = requests.get(url)
        word = r.content[1:-1]
        if (isblacklisted(word)):
            return word
        else:
            return False
            print "blacklisted: %s" % word
    except requests.exceptions.RequestException as e:
        return False
        print e

def request():
    word = ""
    temp = get_word_from_api("http://localhost:8080")
    if (temp):
        word = temp
        print word
        threading.Timer(2.0, request).start()
    else:
        word = get_word_from_list()
        print word
        threading.Timer(2.0, request).start()

print isblacklisted("my friend")
# print isblacklisted("cocks cocks")
