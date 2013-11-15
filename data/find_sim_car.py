import json
import matplotlib.pyplot as plt
import numpy as np
import math 
import pymongo 

from pymongo import MongoClient
client = MongoClient('sd-work2.ece.vt.edu', 27017)
db = client.baseball
collection = db.career_stats

allstats = ['BB%','K%','ISO','BABIP','AVG','SLG', \
            'WAR','H','RBI','SB','OBP','wOBA','wRC+','HR','PA']

maxs = [-1e6 for i in range(len(allstats))]
mins = [1e6 for i in range(len(allstats))]
qry = collection.find()
allp = []
for p in qry:
    for i in range(len(allstats)):
        s = allstats[i]
        st = p[s]
        if st:
            if st > maxs[i]: maxs[i] = st
            if st < mins[i]: mins[i] = st
    if p['name'] not in allp: allp.append(p['name'])

net = {}
distcoll = db.player_dists_car
distcoll.ensure_index('player1')

dists = []
qry = collection.find()
players = [y for y in qry]

for j in range(len(allp)):
    p = allp[j]
    print j
    qry = [y for y in players if y['name'] == p]
    ls = []
    #print 'len '+str(len(qry))+' '+str(maxage)
    for yr in qry:
        qry2 = [y for y in players if y['name'] != p]
        pp = []
        for yr2 in qry2:
            dist = 0;
            for i in range(len(allstats)):
                s = allstats[i]
                if s not in yr or s not in yr2: continue
                if isinstance(yr[s],float) and isinstance(yr2[s],float) and \
                    not math.isnan(yr[s]) and not math.isnan(yr2[s]):
                    dist += (abs(yr[s] - yr2[s])/abs(maxs[i]-mins[i]))**2

            dist = np.sqrt(dist)
            ls.append({'player1':p,'player2':yr2['name'],'dist':dist})


    if ls: distcoll.insert(ls)

