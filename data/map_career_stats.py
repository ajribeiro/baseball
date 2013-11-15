import json
import matplotlib.pyplot as plt
import numpy as np
import math 
import pymongo 


f = open('baseball3.json','r')

data = f.read()

data = json.loads(data)

seasons = data['careers']

from pymongo import MongoClient
client = MongoClient('sd-work2.ece.vt.edu', 27017)
db = client.baseball
collection = db.career_stats
collection.ensure_index('name')
collection.ensure_index('idnum')

ratstats = ['BB%','K%','ISO','BABIP','AVG','SLG']
allstats = ratstats + ['WAR','H','RBI','SB','OBP','wOBA','wRC+','HR','PA']

players = []
for s in seasons:
    name = s['name'].encode('utf-8')
    idnum = s['id']
    p = {}
    p['name'] = name
    p['idnum'] = idnum
    for st in allstats:
        p[st] = s[st]

    players.append(p)

collection.insert(players)
