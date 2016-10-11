__author__ = 'amrit'

import matplotlib.pyplot as plt
import os, pickle
import operator
import numpy as np
import matplotlib.cm as cmx
import matplotlib.colors as colors

#tuned={'pitsE':0.69, 'pitsA':0.64, 'pitsB':0.68, 'pitsC':0.83, 'pitsD': 0.88, 'pitsF':0.67}

#untuned_10={'pitsE':0.62, 'pitsA':0.70, 'pitsB':0.69, 'pitsC':0.78, 'pitsD': 0.85, 'pitsF':0.65}
#untuned_7={'pitsE':0.56, 'pitsA':0.65, 'pitsB':0.63, 'pitsC':0.65, 'pitsD': 0.80, 'pitsF':0.60}

if __name__ == '__main__':

    fileB = ['pitsA', 'pitsB' ,'pitsC','pitsD','pitsE','pitsF']
    '''result1={}
    current_dic1={}
    para_dict1={}
    time1={}
    path = '/home/amrit/GITHUB/Pits_lda/src/06-17/dump/FCR_VEM/test'
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            a = os.path.join(root, name)
            with open(a, 'rb') as handle:
                result = pickle.load(handle)
                result1 = dict(result1.items() + result.items())
                #current_dic = pickle.load(handle)
                #current_dic1 = dict(current_dic1.items() + current_dic.items())
                #para_dict = pickle.load(handle)
                #para_dict1 = dict(para_dict1.items() + para_dict.items())
                #time = pickle.load(handle)
                #time1 = dict(time1.items() + time.items())
    print(para_dict1)
    print(result1)
    print(current_dic1)
    print(time1)'''

    font = {
            'size'   : 60}

    plt.rc('font', **font)
    paras={'lines.linewidth': 10,'legend.fontsize': 35, 'axes.labelsize': 60, 'legend.frameon': False,'figure.autolayout': True}
    plt.rcParams.update(paras)
    X = range(len(fileB))
    plt.figure(num=0, figsize=(25, 15))

    tuned={'pitsE':0.69, 'pitsA':0.64, 'pitsB':0.68, 'pitsC':0.83, 'pitsD': 0.88, 'pitsF':0.67}

    untuned_10={'pitsE':0.62, 'pitsA':0.70, 'pitsB':0.69, 'pitsC':0.78, 'pitsD': 0.85, 'pitsF':0.65}
    untuned_7={'pitsE':0.56, 'pitsA':0.65, 'pitsB':0.63, 'pitsC':0.65, 'pitsD': 0.80, 'pitsF':0.60}


    Y_tuned = []
    Y_untuned = []
    Y_un=[]
    for file1 in fileB:
        Y_tuned.append(tuned[file1])
        Y_untuned.append(untuned_10[file1])
        Y_un.append(untuned_7[file1])
    line, = plt.plot(X, Y_tuned,marker='o', markersize=20, label='tuned 7 words')
    plt.plot(X, Y_untuned, linestyle="-.", marker='*', markersize=20, label='untuned 10 words')
    plt.plot(X, Y_un, linestyle="-.", marker='*', markersize=20, label='untuned 7 words')
    #plt.ytext(0.04, 0.5, va='center', rotation='vertical', fontsize=11)
    #plt.text(0.04, 0.5,"Rn (Raw Score)", labelpad=100)
    #plt.ylim(-0.2,1.1, )
    plt.xticks(X, fileB)
    plt.ylabel("Document Topic % Correctness", labelpad=30)
    plt.xlabel("Datasets",labelpad=30)
    plt.legend(bbox_to_anchor=(0.35, 0.9), loc=1, ncol = 1, borderaxespad=0.)
    plt.savefig("stability" + ".png")
