#!/usr/bin/env python
import requests
import threading
import random

blacklist = ["Jacob", "William", "Ethan", "James", "Alexander", "Jackson", "David", "Oliver", "Jayden", "Joseph", "Gabriel", "Samuel", "Carter", "Anthony", "John", "Dylan", "Luke", "Henry", "Andrew", "Isaac", "Christopher", "Joshua", "Wyatt", "Sebastian", "Owen", "Caleb", "Nathan"]

loop = [ "man", "design", "branding", "advertising", "typography", "photography", "illustration", "editorial", "video", "print", "web"]

def print_on_led_matrix(word):
    print word

def blacklisted(word):
    if (word in blacklist):
        return False
    else:
        return True

def request():
    r = requests.get('http://localhost:8080')
    word = r.content.strip('"')
    if (r.status_code == 200):
        if (blacklisted(word) and word != "empty"):
            # time.sleep(2.0)
            threading.Timer(2.0, request).start()
            print_on_led_matrix(word)
        elif(word == "empty"):
            threading.Timer(2.0, request).start()
            print "-"
            print_on_led_matrix(loop[random.randint(0,len(loop)-1)])
        else:
            print "blacklisted: %s" % word
            request()
    else:
        print "not found!!"

request()
