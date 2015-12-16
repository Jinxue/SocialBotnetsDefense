'''
Created on Mar 22, 2015

@author: Jinxue Zhang

Obtain the edges of the different edges
'''

for dataset in ['TS', 'PI', 'CI', 'LA']:
    for networktype in ['friends', 'interactions']:
        edges = 0
        weights = 0
        for line in open('E:\\BotnetDefense\\' + dataset + '\\' + networktype + '-local.txt', 'r'):
            if not line.startswith('%'):
                edges += 1
            else:
                weights += int(line.split(',')[3])
        print dataset, networktype, edges, weights