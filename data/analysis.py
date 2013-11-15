import json
import matplotlib.pyplot as plt
import numpy as np
import math 
import pymongo 

dists = {}
ids = {}
stats = []
maxs,mins = [],[]

def add_node(g,p1,p2,w):
    if p1 not in g: g[p1] = {}
    g[p1][p2] = w
    if p2 not in g: g[p2] = {}
    g[p2][p1] = w

def add_node2(g,p1,p2,w,age):
    if p1 not in g: g[p1] = {}
    g[p1][p2] = {}
    g[p1][p2][age] = w
    if p2 not in g: g[p2] = {}
    g[p2][p1] = {}
    g[p2][p1][age] = w

        
def calc_avgs(p1,averages,mx):
    averages[p1] = {}
    maxage = max(players[p1].keys())
    averages[p1]['maxage'] = maxage
    alls = [[] for i in range(len(stats))]
    for a in players[p1]:
        if a > mx: continue
        for i in range(len(stats)):
            s = stats[i]
            if players[p1][a][s]:
                alls[i].append(players[p1][a][s])

        avgs = [np.mean(b) for b in alls]

        averages[p1][a] = avgs

def calc_sim(averages,p,p2,stats,dists,mx,ids):
    for a in range(0,mx):
        if a not in averages[p] or a not in averages[p2]: continue
        dist = 0;
        for i in range(len(stats)):
            if not math.isnan(averages[p][a][i]) and not math.isnan(averages[p2][a][i]) and isinstance(averages[p][a][i],float) and isinstance(averages[p2][a][i],float):
                dist += (abs(averages[p][a][i] - averages[p2][a][i])/abs(maxs[i]-mins[i]))**2

        add_node2(dists,ids[p],ids[p2],sim,a)
        

def calc_sim_car(averages,p,p2,stats,dists,mx,ids):
    if p in dists and p2 in dists[p]: return
    if p == p2: return

    mx = averages[p]['maxage']
    mx2 = averages[p2]['maxage']
    dist = 0.
    for i in range(len(stats)):
        if not math.isnan(averages[p][mx][i]) and not math.isnan(averages[p2][mx2][i]) \
            and isinstance(averages[p][mx][i],float) and isinstance(averages[p2][mx2][i],float):
            dist += (abs(averages[p][mx][i] - averages[p2][mx2][i])/abs(maxs[i]-mins[i]))**2

    dist = np.sqrt(dist)
    add_node(dists,ids[p],ids[p2],dist)


f = open('baseball3.json','r')

data = f.read()

data = json.loads(data)

seasons = data['seasons']

from pymongo import MongoClient
client = MongoClient('sd-work2.ece.vt.edu', 27017)
db = client.baseball
collection = db.player_stats
collection.ensure_index('name')
collection.ensure_index('age')
collection.ensure_index('idnum')

ratstats = ['HR%','R%','SB%','BB%','K%','ISO','BABIP','AVG','SLG','BsR']
allstats = ratstats + ['WAR','H','RBI','SB','OBP','wOBA','wRC+','HR','PA','AB','G']

# players = []
# for s in seasons:
#     name = s['name'].encode('utf-8')
#     idnum = s['id']
#     # if idnum not in players:
#     #     # players[idnum] = {}
#     #     ids[idnum] = name

#     age = int(s['Age'])

#     p = {}
#     p['age'] = age
#     p['name'] = name
#     p['idnum'] = idnum
#     for st in allstats:
#         if st == 'HR%':
#             p[st] = s['HR']/float(s['AB'])
#         elif st == 'R%':
#             p[st] = s['R']/float(s['AB'])
#         elif st == 'SB%':
#             p[st] = s['SB']/float(s['PA'])
#         else:
#             p[st] = s[st]

#     players.append(p)

# collection.insert(players)

maxs = [-1e6 for i in range(len(ratstats))]
mins = [1e6 for i in range(len(ratstats))]
qry = collection.find()
allp = []
for p in qry:
    for i in range(len(ratstats)):
        s = ratstats[i]
        st = p[s]
        if st:
            if st > maxs[i]: maxs[i] = st
            if st < mins[i]: mins[i] = st
    allp.append(p['name'])

averages = []
for j in range(len(allp)):
    p = allp[j]
    print j
    q = collection.find({'name':p})
    print 'count '+str(q.count())
    if q.count() < 1: continue
    q = [y for y in q]
    maxage = max([y['age'] for y in q])
    minage = min([y['age'] for y in q])

    for age in range(minage,maxage+1):
        qry = [y for y in q if y['age'] < age]
        avg = {'name':p,'age':age}
        for i in range(len(ratstats)):
            s = ratstats[i]
            weights = []
            alls = []
            n = 0
            for yr in qry:
                avg['idnum'] = yr['idnum']
                if yr[s]:
                    alls.append(yr[s])
                    weights.append(yr['PA'])

            if alls:
                avg[ratstats[i]] = np.average(alls,weights=weights)

        averages.append(avg)

avgcoll = db.player_averages
avgcoll.ensure_index('name')
avgcoll.ensure_index('age')
avgcoll.ensure_index('idnum')
avgcoll.insert(averages)


net = {}
distcoll = db.player_dists
distcoll.ensure_index('player1')
distcoll.ensure_index('player2')
distcoll.ensure_index('age')

dists = []
qry = avgcoll.find()
players = [y for y in qry]

# for j in range(len(allp)):
#     p = allp[j]
#     print j
#     qry = [y for y in players if y['name'] == p]
#     maxage = max([y['age'] for y in qry]) 
#     qry = [y for y in qry if y['age'] == maxage]
#     print qry
#     ls = []
#     print 'len '+str(len(qry))+' '+str(maxage)
#     for yr in qry:
#         qry2 = [y for y in players if y['age'] == maxage and y['name'] != p]
#         # print 'len2 '+str(len(qry2))
#         # qry2 = avgcoll.find({'name':{'$ne':p},'age':yr['age']})
#         pp = []
#         for yr2 in qry2:
#             if p in net and yr2['name'] in net[p]: continue
#             dist = 0;
#             for i in range(len(ratstats)):
#                 s = ratstats[i]
#                 if s not in yr or s not in yr2: continue
#                 if not math.isnan(yr[s]) and not math.isnan(yr2[s]) and \
#                         isinstance(yr[s],float) and isinstance(yr2[s],float):
#                     dist += (abs(yr[s] - yr2[s])/abs(maxs[i]-mins[i]))**2

#             dist = np.sqrt(dist)
#             pp.append(yr2['name'])
#             ls.append({'player1':p,'player2':yr2['name'],'age':yr['age'],'dist':dist})

#         for p2 in pp:
#             add_node(net,p,p2,dist)

#     if ls: distcoll.insert(ls)




# averages = {}
# import datetime as dt
# t1 = dt.datetime.now()
# map(lambda x: calc_avgs(x,averages, 1e6), players)
# print dt.datetime.now()-t1

# for p in averages:
#     k = averages[p].keys()
#     k.remove('maxage')
#     mx = max(k)
#     map(lambda p2: calc_sim_car(averages,p,p2,stats,dists,mx,ids), averages)


