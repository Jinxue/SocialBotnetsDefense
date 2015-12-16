'''
Created on Aug 14, 2015

@author: Obtain the average results

Jinxue Zhang
'''

res = dict()

rounds = 100

for line in open('E:\\BotnetDefense\\results-interaction-attack2-sep-LA.txt', 'rb'):
    if not line.startswith('LA'):
        continue
    items = line.split()
    
    x = float(items[1])
    if x not in res:
        res[x] = []
        for i in range(5):
            res[x].append(0)
            
    res[x][0] += float(items[3])
    res[x][1] += float(items[4])
    res[x][2] += int(items[5])
    res[x][3] += int(items[6])
    res[x][4] += float(items[7])

for x in res:
    for i in range(5):
        res[x][i] = 1.0 * res[x][i] / 100

res_sorted = sorted(res.items(), key=lambda x: x[0])
for x, y in res_sorted:
    print y[0], y[1], y[2], y[3], y[4]