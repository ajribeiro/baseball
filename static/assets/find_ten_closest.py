import matplotlib.pyplot as plt
import numpy as np
import math 
import pymongo 


from pymongo import MongoClient
client = MongoClient('sd-work2.ece.vt.edu', 27017)
db = client.baseball
collection = db.player_stats

ratstats = ['HR%','R%','SB%','BB%','K%','ISO','BABIP','AVG','SLG','BsR']
allstats = ratstats + ['WAR','H','RBI','SB','OBP','wOBA','wRC+','HR','PA','AB','G']

allplayers = []
qry = collection.find()
for p in qry:
    if p['name'] not in allplayers: allplayers.append(p['name'])

dists = db.player_dists
tens = db.top_tens
tens.ensure_index('name')

for i in range(len(allplayers)):
    print i
    p = allplayers[i]
    qry = dists.find({'player1':p})
    qry = [q for q in qry]
    qry = sorted(qry,key=lambda k: k['dist'])
    if len(qry) >= 10:
        qry = qry[:10]
    else:
        qry = qry[:len(qry)]

    ls = {'name':p,'age':qry[0]['age'],'ten':[{'other':x['player2'],'dist':x['dist']} for x in qry]}

    tens.insert(ls)
