#!/usr/bin/env python
import requests
r = requests.get('http://localhost:8080')
print r.content
