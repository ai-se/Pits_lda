__author__ = 'amrit'

import matplotlib.pyplot as plt
import os, pickle
# Untuned

#https://docs.google.com/a/ncsu.edu/spreadsheets/d/1kLAHoSQzf4QGEhlGBcpmkukMWpaTPsEeNSMl1kVIj2I/edit?usp=sharing
#{'processed_citemap.txt': {1: 0.90000000000000002, 2: 0.90000000000000002, 3: 0.90000000000000002, 4: 0.80000000000000004, 5: 0.64999999999999991, 6: 0.5, 7: 0.29999999999999999, 8: 0.20000000000000001, 9: 0.10000000000000001}}
#{'stack': {1: 0.90000000000000002, 2: 0.90000000000000002, 3: 0.90000000000000002, 4: 0.90000000000000002, 5: 0.90000000000000002, 6: 0.80000000000000004, 7: 0.64999999999999991, 8: 0.55000000000000004, 9: 0.69999999999999996}}

#

if __name__ == '__main__':
    result1 = {}
    x1={}
    path = '/home/amrit/GITHUB/Pits_lda/src/05-25/results/Citemap_nostem/dump'
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            a = os.path.join(root, name)
            with open(a, 'rb') as handle:
                result = {}
                x={}
                result = pickle.load(handle)
                x=pickle.load(handle)
                # print(F_final)
                result1 = dict(result1.items() + result.items())
                x1=dict(x1.items() + x.items())
    print(result1)
    print(x1)
    untuned = {'nostem_citemap.txt': {1: 0.90000000000000002, 2: 0.90000000000000002, 3: 0.90000000000000002, 4: 0.80000000000000004, 5: 0.64999999999999991, 6: 0.5, 7: 0.29999999999999999, 8: 0.20000000000000001, 9: 0.10000000000000001}}

    result=['F3CR7pop10','F7CR3pop10']#, 'F7CR3pop30','F3CR7pop30']

    labels = [1,2,3,4, 5, 6, 7, 8, 9]
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 20}

    plt.rc('font', **font)
    paras={'lines.linewidth': 5,'legend.fontsize': 20, 'axes.labelsize': 30, 'legend.frameon': False,'figure.autolayout': True,'figure.figsize': (16,8)}
    plt.rcParams.update(paras)
    X = range(len(labels))
    plt.figure(num=0, figsize=(25, 15))
    #plt.subplot(121)
    Y_untuned=[]

    for x in result:
        Y_tuned=[]
        for lab in labels:
            Y_tuned.append(result1[x][lab])
        line, = plt.plot(X, Y_tuned, marker='o', markersize=16, label='tuned_'+x+'_citemap')
    for lab in labels:
        Y_untuned.append(untuned['nostem_citemap.txt'][lab])

    plt.plot(X,Y_untuned,"-.", marker='o', markersize=16, label='untuned_citemap')
    plt.xticks(X, labels)
    plt.ylabel("Stability Scores")
    plt.xlabel("No of terms overlap")
    plt.legend(bbox_to_anchor=(0.95, 0.5), loc=1, ncol = 1, borderaxespad=0.)
    plt.savefig("tuned_citemap_nostem" + ".png")