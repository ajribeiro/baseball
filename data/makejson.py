import string
import os
import json


f = open('baseball3.csv','r')
fj = open('baseball3.json','w')

header = f.readline()
columns = header.split(',')
for i in range(len(columns)): columns[i] = columns[i].replace("\"",'')
#set up all of the indices



allplayers = []
for line in f:
    c = line.split(',')
    for i in range(len(c)): c[i] = c[i].replace("\"",'')

    idnum = int(c[-1])
    p = {'id':idnum,'name':c[1],'year':int(c[0])}
    
    for i in range(3,len(c)-1):
        if c[i] != ' ':
            p[columns[i]] = float(string.replace(c[i],'%',''))
        else:
            p[columns[i]] = None

    p['hsh'] = c[1].replace(' ','').replace(".",'').replace("'",'')+str(int(c[0]))+str(idnum)
    p['lname'] = c[1].replace(' ','').replace(".",'').replace("'",'').lower()
    allplayers.append(p)

f.close()


f = open('career2.csv','r')
header = f.readline()
columns = header.split(',')
for i in range(len(columns)): columns[i] = columns[i].replace("\"",'')
allcars = []
for line in f:
    c = line.split(',')
    for i in range(len(c)): c[i] = c[i].replace("\"",'')

    idnum = int(c[-1])
    p = {'id':idnum,'name':c[0]}
    
    for i in range(3,len(c)-1):
        if c[i] != ' ':
            p[columns[i]] = float(string.replace(c[i],'%',''))
        else:
            p[columns[i]] = None

    p['hsh'] = c[0].replace(' ','').replace(".",'').replace("'",'')+str(idnum)

    allcars.append(p)

ps = {'seasons': allplayers, 'careers': allcars}
fj.write(json.dumps(ps))

f.close()

fj.close()