import string
import os
import json


f = open('baseball.csv','r')
fj = open('baseball.json','w')

header = f.readline()
columns = header.split(',')
#set up all of the indices



allplayers = []
for line in f:
    c = line.split(',')
    idnum = int(c[-1])
    p = {'id':idnum,'name':c[1],'year':int(c[0])}
    
    for i in range(3,len(c)-1):
        if c[i] != ' ':
            p[columns[i]] = float(string.replace(c[i],'%',''))
        else:
            p[columns[i]] = None

    p['hsh'] = c[1].replace(' ','').replace(".",'').replace("'",'')+str(int(c[0]))
    allplayers.append(p)

f.close()


f = open('career.csv','r')
header = f.readline()
columns = header.split(',')

allcars = []
for line in f:
    c = line.split(',')
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