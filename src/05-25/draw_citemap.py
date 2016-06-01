__author__ = 'amrit'

import matplotlib.pyplot as plt
import os, pickle
# Untuned

#https://docs.google.com/a/ncsu.edu/spreadsheets/d/1kLAHoSQzf4QGEhlGBcpmkukMWpaTPsEeNSMl1kVIj2I/edit?usp=sharing
#{'processed_citemap.txt': {1: 0.90000000000000002, 2: 0.90000000000000002, 3: 0.90000000000000002, 4: 0.80000000000000004, 5: 0.64999999999999991, 6: 0.5, 7: 0.29999999999999999, 8: 0.20000000000000001, 9: 0.10000000000000001}}

#

if __name__ == '__main__':
    result1 = {}
    path = '/home/amrit/GITHUB/Pits_lda/src/05-25/dump'
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            a = os.path.join(root, name)
            with open(a, 'rb') as handle:
                result = {}
                result = pickle.load(handle)
                # print(F_final)
                result1 = dict(result1.items() + result.items())

    untuned={'processed_citemap.txt': {1: 0.90000000000000002, 2: 0.90000000000000002, 3: 0.90000000000000002, 4: 0.80000000000000004, 5: 0.64999999999999991, 6: 0.5, 7: 0.29999999999999999, 8: 0.20000000000000001, 9: 0.10000000000000001}}

    result=['F3CR7pop10','F7CR3pop10', 'F7CR3pop30','F3CR7pop30']

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
    for a in result:
        Y_tuned=[]
        Y_untuned=[]
        Y_final=[]
        for lab in labels:
            Y_tuned.append(result1[a][lab])
            Y_untuned.append(untuned['processed_citemap.txt'][lab])
        for i,x in enumerate(Y_untuned):
            Y_final.append(Y_tuned[i]-x)
        line, = plt.plot(X, Y_final, marker='o', markersize=16, label=a + '_citemap')
    plt.xticks(X, labels)
    plt.ylabel("% of performance improvement")
    plt.xlabel("No of terms overlap")
    plt.legend(bbox_to_anchor=(0.95, 0.5), loc=1, ncol = 1, borderaxespad=0.)
    plt.savefig("tuned_citemap" + ".png")
