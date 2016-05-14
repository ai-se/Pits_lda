__author__ = 'amrit'

import matplotlib.pyplot as plt
import numpy as np
import os
import pickle

if __name__ == '__main__':
    # "draw"
    result1 = {}
    path = '/home/amrit/GITHUB/Pits_lda/src/05-05/hpc/dump'
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            a = os.path.join(root, name)
            with open(a, 'rb') as handle:
                result = {}
                result = pickle.load(handle)
                # print(F_final)
                result1 = dict(result1.items() + result.items())
    filenamelist = ['101pitsA_2.txt', '101pitsB_2.txt', '101pitsC_2.txt', '101pitsD_2.txt', '101pitsE_2.txt',
                    '101pitsF_2.txt']
    labels = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    untuned={'101pitsF_2.txt': {1: 0.90000000000000002, 2: 0.90000000000000002, 3: 0.90000000000000002, 4: 0.90000000000000002, 5: 0.59999999999999998, 6: 0.5, 7: 0.5, 8: 0.25, 9: 0.5}, '101pitsE_2.txt': {1: 0.90000000000000002, 2: 0.90000000000000002, 3: 0.90000000000000002, 4: 0.80000000000000004, 5: 0.69999999999999996, 6: 0.40000000000000002, 7: 0.29999999999999999, 8: 0.40000000000000002, 9: 0.59999999999999998}, '101pitsA_2.txt': {1: 0.90000000000000002, 2: 0.90000000000000002, 3: 0.90000000000000002, 4: 0.90000000000000002, 5: 0.69999999999999996, 6: 0.5, 7: 0.20000000000000001, 8: 0.15000000000000002, 9: 0.10000000000000001}, '101pitsC_2.txt': {1: 0.90000000000000002, 2: 0.90000000000000002, 3: 0.90000000000000002, 4: 0.90000000000000002, 5: 0.90000000000000002, 6: 0.55000000000000004, 7: 0.55000000000000004, 8: 0.80000000000000004, 9: 0.80000000000000004}, '101pitsB_2.txt': {1: 0.90000000000000002, 2: 0.90000000000000002, 3: 0.90000000000000002, 4: 0.90000000000000002, 5: 0.80000000000000004, 6: 0.59999999999999998, 7: 0.5, 8: 0.29999999999999999, 9: 0.20000000000000001}, '101pitsD_2.txt': {1: 0.90000000000000002, 2: 0.90000000000000002, 3: 0.90000000000000002, 4: 0.90000000000000002, 5: 0.80000000000000004, 6: 0.59999999999999998, 7: 0.29999999999999999, 8: 0.20000000000000001, 9: 0.25}}

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
    for file1 in filenamelist:
        Y_tuned=[]
        Y_untuned=[]
        Y_final=[]
        for lab in labels:
            Y_tuned.append(result1[file1][lab])
            Y_untuned.append(untuned[file1][lab])
        for i,x in enumerate(Y_untuned):
            Y_final.append(Y_tuned[i]-x)
        line, = plt.plot(X, Y_final, marker='o', markersize=16, label="tuned-untuned" + file1)
    plt.xticks(X, labels)
    plt.ylabel("% of performance improvement")
    plt.xlabel("No of terms overlap")
    plt.legend(bbox_to_anchor=(0.95, 0.5), loc=1, ncol = 1, borderaxespad=0.)
    plt.savefig("tuned_F3CR7pop30" + ".png")
