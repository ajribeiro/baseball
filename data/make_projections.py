import matplotlib.pyplot as plt
import numpy as np
import math 
import pymongo 


from pymongo import MongoClient
client = MongoClient('sd-work2.ece.vt.edu', 27017)
db = client.baseball


ratstats = ['HR%','R%','SB%','BB%','K%','ISO','BABIP','AVG','SLG','BsR']
allstats = ratstats + ['WAR','H','RBI','SB','OBP','wOBA','wRC+','HR','PA','AB','G']


stats = db.player_stats
proj = db.player_proj
dists = db.player_dists

proj.ensure_index('name')


allplayers = []
qry = stats.find()
for p in qry:
    if p['name'] not in allplayers: allplayers.append(p['name'])



for i in range(len(allplayers)):
    print i
    p = allplayers[i]
    qry = dists.find({'player1':p})
    qry = [q for q in qry]
    qry = sorted(qry,key=lambda k: k['dist'])

    start_age = qry[0]['age']
    name = p
    pdict = {'name':name,'projs':[]}

    age = start_age+1
    while 1:
        weights,others = [],[] 
        for p2 in qry:
            if len(others) >= 10: break
            qry2 = stats.find({'name':p2['player2'],'age':age})
            if qry2.count() < 1: continue
            qry2 = [q for q in qry2]
            others.append(qry2[0])
            weights.append(p2['dist'])

        if len(others) < 10: break

        pd = {'age':age}
        for s in allstats:
            ls = []
            for o in others:
                ls.append(o[s])
            if None in ls: continue
            m = np.average(ls,weights=1./np.array(weights))
            pd[s] = m
        pdict['projs'].append(pd)
        age += 1
    proj.insert(pdict)


# qry = tens.find()
# qry = [q for q in qry]
# for i in range(len(qry)):
#     print i
#     p = qry[i]
#     start_age = p['age']
#     name = p['name']
#     weights,others = [],[] 
#     for p2 in p['ten']:
#         weights.append(p2['dist'])
#         others.append(p2['other'])

#     pdict = {'name':name,'projs':[]}
#     age = start_age
#     while 1:
#         knn_stats = []

#         for p2 in others:
#             qry2 = stats.find({'name':p2,'age':age})
#             if qry2.count() < 1: continue
#             knn_stats.append([q for q in qry2][0])

#         print len(knn_stats),start_age
#         if len(knn_stats) < 10: break

#         pd = {'age':age}
#         for s in allstats:
#             ls = []
#             for k in knn_stats:
#                 ls.append(k[s])
#             if None in ls: continue
#             m = np.average(ls,weights=weights)
#             pd[s] = m
#         pdict['projs'].append(pd)
#         proj.insert(pdict)

#         age += 1
