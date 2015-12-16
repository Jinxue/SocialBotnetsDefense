'''
Created on Mar 21, 2015

@author: Jinxue Zhang
Obtain the incoming interactions from the outgoing interaction file
'''

dataset = 'TS'
path = 'E:\\BotnetDefense\\' + dataset + '\\'
inputF = path + 'interactions-local.txt'

outF = open(path + 'interactions-incoming-local.txt', 'w')

incoming = dict()

edges = 0
for line in open(inputF, 'r'):
    if line.startswith('%'):
        items = line.rstrip('\r\n').split(',')
        if len(items) < 4:
            print line
            continue
        else:
            srcid = items[0][1:]
    else:
        items = line.rstrip('\r\n').split(',')
        if len(items) < 2:
            print line
            continue
        else:
            if items[0] not in incoming:
                incoming[items[0]] = dict()
            incoming[items[0]][srcid] = int(items[1])
    if edges % 1000000 == 0:
        print 'finished loading ', edges, 'edges.'
    edges += 1

for user in incoming:
    totalWeights = 0
    for follower in incoming[user]:
        totalWeights += incoming[user][follower]
    print >> outF, '%' + user + ',' + '0,' + str(len(incoming[user])) + ',' + str(totalWeights)
    for follower in incoming[user]:
        print >>outF, follower + ',' + str(incoming[user][follower])