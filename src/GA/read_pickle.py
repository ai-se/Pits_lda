from __future__ import print_function, division

__author__ = 'amritanshu.agrawal'

import sys

sys.dont_write_bytecode = True
import pickle
import os
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

tuned_gibbs = {
    'pitsF': {1: 1.0, 2: 1.0, 3: 1.0, 4: 1.0, 5: 0.8888888888888888, 6: 0.6666666666666666, 7: 0.5555555555555556,
              8: 0.6666666666666666, 9: 0.8888888888888888},
    'pitsE': {1: 1.0, 2: 1.0, 3: 1.0, 4: 1.0, 5: 0.8888888888888888, 6: 0.6666666666666666, 7: 0.5555555555555556,
              8: 0.7777777777777778, 9: 0.7777777777777778},
    'pitsD': {1: 1.0, 2: 1.0, 3: 1.0, 4: 1.0, 5: 1.0, 6: 0.8888888888888888, 7: 0.7777777777777778,
              8: 0.7777777777777778, 9: 0.4444444444444444},
    'pitsC': {1: 1.0, 2: 1.0, 3: 1.0, 4: 1.0, 5: 1.0, 6: 1.0, 7: 1.0, 8: 1.0, 9: 0.6666666666666666},
    'pitsB': {1: 1.0, 2: 1.0, 3: 1.0, 4: 1.0, 5: 0.8888888888888888, 6: 0.6666666666666666, 7: 0.5555555555555556,
              8: 0.6666666666666666, 9: 0.5555555555555556},
    'pitsA': {1: 1.0, 2: 1.0, 3: 1.0, 4: 1.0, 5: 0.8888888888888888, 6: 0.6666666666666666, 7: 0.5555555555555556,
              8: 0.4444444444444444, 9: 0.3333333333333333}}
delta_de_ga={'pitsF': [0.0, 0.0, 0.0, 0.0, 0.11111111111111116, 0.2222222222222222, 0.33333333333333326, 0.11111111111111116, 0.11111111111111105], 'pitsE': [0.0, 0.0, 0.0, 0.0, 0.11111111111111116, 0.11111111111111116, 0.2222222222222222, 0.2222222222222222, 0.2222222222222222], 'pitsD': [0.0, 0.0, 0.0, 0.0, 0.0, 0.11111111111111116, 0.2222222222222222, -0.11111111111111116, 0.2222222222222222], 'pitsC': [0.0, 0.0, 0.0, 0.0, 0.0, -0.2222222222222222, -0.2222222222222222, -0.11111111111111116, -0.11111111111111116], 'pitsB': [0.0, 0.0, 0.0, 0.0, 0.11111111111111116, 0.11111111111111116, 0.0, -0.11111111111111116, -0.11111111111111116], 'pitsA': [0.0, 0.0, 0.0, 0.0, 0.11111111111111116, 0.2222222222222222, 0.2222222222222222, 0.11111111111111116, 0.1111111111111111]}

if __name__ == '__main__':
    result1={}
    path='/Users/amrit/GITHUB/Pits_lda/src/GA/dump/'
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            a = os.path.join(root, name)
            with open(a, 'rb') as handle:
                result = {}
                result = pickle.load(handle)
                # print(F_final)
                result1 = dict(result1.items() + result.items())

    runtime={}
    for i in result1.keys():
        runtime[i]=result1[i][-1]
    score={}
    for a,b in result1.iteritems():
        score[a]=[]
        for c,d in b[0].iteritems():
            score[a].append(d[-1])
    print(runtime)
    print(score)
    score1={}
    for a,b in tuned_gibbs.iteritems():
        score1[a]=[]
        for x,y in b.iteritems():
            score1[a].append(y)

    print(score1)
    temp={}
    for x,y in score.iteritems():
        temp[x]=[a_i - b_i for a_i, b_i in zip(score[x], score1[x])]
    print(temp)

    font = {'family': 'normal',
            'weight': 'bold',
            'size': 70}

    plt.rc('font', **font)
    paras = {'lines.linewidth': 8, 'legend.fontsize': 60, 'axes.labelsize': 70, 'legend.frameon': False,
             'figure.autolayout': True, 'figure.figsize': (16, 8)}
    plt.rcParams.update(paras)
    fileB=score.keys()
    X = range(1,10)
    plt.figure(num=0, figsize=(40, 25))

    for file in fileB:
        line, = plt.plot(X, temp[file], marker='o', markersize=16, label=file)

    plt.xticks(X, range(1,10))
    plt.ylabel("Delta LDADE - LDAGA")
    plt.xlabel("No of terms overlap")
    plt.legend(bbox_to_anchor=(0.3, 0.8), loc=1, ncol = 1, borderaxespad=0.)
    plt.savefig("ldaga_noorder" + ".png")