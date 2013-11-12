
import json
import matplotlib.pyplot as plt
import numpy as np
import math 

dists = {}
ids = {}
stats = []
maxs,mins = [],[]

def add_node(g,p1,p2,w):
    if p1 not in g: g[p1] = {}
    g[p1][p2] = w
    if p2 not in g: g[p2] = {}
    g[p2][p1] = {}

        
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

    # for a in alls:
    #     avgs.append(np.mean(a))

# def outer_loop(p1, averages, players):
#     print ids[p1]
#     maxage = averages[p1]['maxage']
#     averages2 = {}
#     map(lambda x: calc_avgs(x,averages2, maxage), players)
#     for i in range(len(stats)):
#         if averages[i] and avgs2[i]:
#             sim += (1.- abs(averages[i] - avgs2[i])/abs(maxs[i]-mins[i]))


def calc_sim(averages,p,p2,stats,dists,mx,ids):
    if mx in averages[p2]:
        sim = 0;
        for i in range(len(stats)):
            if not math.isnan(averages[p][mx][i]) and not math.isnan(averages[p2][mx][i]) and isinstance(averages[p][mx][i],float) and isinstance(averages[p2][mx][i],float):
                # print stats[i],averages[p][mx][i], averages[p2][mx][i],maxs[i],mins[i],maxs[i]-mins[i], abs(averages[p][mx][i] - averages[p2][mx][i])/abs(maxs[i]-mins[i])
                sim += (1.- abs(averages[p][mx][i] - averages[p2][mx][i])/abs(maxs[i]-mins[i]))

        add_node(dists,ids[p],ids[p2],sim)
        

def calc_sim_car(averages,p,p2,stats,dists,mx,ids):
    mx = averages[p]['maxage']
    mx2 = averages[p2]['maxage']
    sim = 0;
    for i in range(len(stats)):
        if not math.isnan(averages[p][mx][i]) and not math.isnan(averages[p2][mx2][i]) \
            and isinstance(averages[p][mx][i],float) and isinstance(averages[p2][mx2][i],float):
            # print stats[i],averages[p][mx][i], averages[p2][mx][i],maxs[i],mins[i],maxs[i]-mins[i], abs(averages[p][mx][i] - averages[p2][mx][i])/abs(maxs[i]-mins[i])
            sim += (1.- abs(averages[p][mx][i] - averages[p2][mx2][i])/abs(maxs[i]-mins[i]))

        add_node(dists,ids[p],ids[p2],sim)
        

f = open('baseball3.json','r')

data = f.read()

data = json.loads(data)

seasons = data['seasons']

players = {}
stats = ['HR%','R%','SB%','BB%','K%','ISO','BABIP','AVG','SLG','BsR']

for s in seasons:
    name = s['name'].encode('utf-8')
    idnum = s['id']
    if idnum not in players:
        players[idnum] = {}
        ids[idnum] = name

    age = int(s['Age'])
    players[idnum][age] = {}
    for st in stats:
        if st == 'HR%':
            players[idnum][age][st] = s['HR']/float(s['AB'])
        elif st == 'R%':
            players[idnum][age][st] = s['R']/float(s['AB'])
        elif st == 'SB%':
            players[idnum][age][st] = s['SB']/float(s['PA'])
        else:
            players[idnum][age][st] = s[st]

maxs = [-1e6 for i in range(len(stats))]
mins = [1e6 for i in range(len(stats))]
for p in players:
    for a in players[p]:
        for i in range(len(stats)):
            s = stats[i]
            st = players[p][a][s]
            if st:
                if st > maxs[i]: maxs[i] = st
                if st < mins[i]: mins[i] = st

averages = {}
map(lambda x: calc_avgs(x,averages, 1e6), players)

# map(lambda x: outer_loop(x,averages, players), averages)

for p in averages:
    k = averages[p].keys()
    k.remove('maxage')
    mx = max(k)
    map(lambda p2: calc_sim_car(averages,p,p2,stats,dists,mx,ids), averages)


# for p1 in players:
#     print p1
#     maxage = max(players[p1].keys())
#     alls = [[] for i in range(len(stats))]
#     for a in players[p1]:
#         alls = [players[p1][a][s] for s in stats if players[p1][a][s]]
#         # for i in range(len(stats)):
#         #     s = stats[i]
#         #     if players[p1][a][s]:
#         #         alls[i].append(players[p1][a][s])
#     avgs = [np.mean(a) for a in alls]
#     # for a in alls:
#     #     avgs.append(np.mean(a))

#     # map(lambda x: calc_sim(players,p1,x,maxage,stats),players)
#     for p2 in players:
#         if p1 == p2 or (p1 in dists and p2 in dists[p1]): continue
#         alls = [[] for i in range(len(stats))]
#         for a in players[p2]:
#             if a > maxage: continue
#             for i in range(len(stats)):
#                 s = stats[i]
#                 if players[p2][a][s]:
#                     alls[i].append(players[p2][a][s])
#         avgs2 = []
#         for a in alls:
#             avgs2.append(np.mean(a))
#         sim = 0.
#         for i in range(len(stats)):
#             if avgs[i] and avgs2[i]:
#                 sim += (1.- abs(avgs[i] - avgs2[i])/abs(maxs[i]-mins[i]))





