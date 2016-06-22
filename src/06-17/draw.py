__author__ = 'amrit'

import matplotlib.pyplot as plt
import os, pickle
import operator
import numpy as np
import matplotlib.cm as cmx
import matplotlib.colors as colors

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                '%d' % int(height),
                ha='center', va='bottom')

def get_cmap(N):
    '''Returns a function that maps each index in 0, 1, ... N-1 to a distinct
    RGB color.'''
    color_norm  = colors.Normalize(vmin=0, vmax=N-1)
    scalar_map = cmx.ScalarMappable(norm=color_norm, cmap='hsv')
    def map_index_to_rgb_color(index):
        return scalar_map.to_rgba(index)
    return map_index_to_rgb_color



if __name__ == '__main__':
    '''result1 = {}
    a1 = {}
    score1 = {}
    path = '/home/amrit/GITHUB/Pits_lda/src/06-03/dump/'
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            a = os.path.join(root, name)
            with open(a, 'rb') as handle:
                result = {}
                a = {}
                score = {}
                result = pickle.load(handle)
                score = pickle.load(handle)
                a = pickle.load(handle)
                # print(F_final)
                result1 = dict(result1.items() + result.items())
                score11 = dict(score1.items() + score.items())
                a1 = dict(a1.items() + a.items())
    # print(result1)
    # print(a1)
    print(score1)'''


    labels = [8, 9]
    iterations = range(1, 5, 1)
    N = 2

    ind = np.arange(N)  # the x locations for the groups
    width = 0.1  # the width of the bars
    font = {'family': 'normal',
            'weight': 'bold',
            'size': 20}
    #cmap = get_cmap(N)
    plt.rc('font', **font)
    paras = {'lines.linewidth': 5, 'legend.fontsize': 20, 'axes.labelsize': 30, 'legend.frameon': False,
             'figure.autolayout': True, 'figure.figsize': (16, 8)}
    plt.rcParams.update(paras)
    f=plt.figure(num=0, figsize=(25, 15))
    colors1 = "bgrcmykw"
    z=[]
    for i,x in enumerate(iterations):
        frequency = []
        for y in labels:
            z = max(score1[y][x].iteritems(), key=operator.itemgetter(0))[0]
            frequency.append(len(score1[y][x][z]))
        plt.bar(ind+i*width , frequency, width=width, color=colors1[i], label='iterations='+str(x*100))


    plt.xlabel("Term Overlaps")
    plt.ylabel('Frequency of parameters')
    plt.xticks(ind + width,labels)
    plt.legend( bbox_to_anchor=(1.0, 0.9), loc=1, ncol=1, borderaxespad=0.)
    f.savefig("frequ_pitsA" + ".png")

    f1=plt.figure(num=1, figsize=(25, 15))
    for i,x in enumerate([1]):
        par_k=[]
        par_a=[]
        par_b=[]
        temp=[]
        for y in labels:
            z = max(score1[y][x].iteritems(), key=operator.itemgetter(0))[0]
            for j in score1[y][x][z]:
                par_k.append(int(j[0]))
                par_a.append(j[1])
                par_b.append(j[2])
            par_k=sorted(par_k)
            par_a=sorted(par_a)
            par_b=sorted(par_b)
            temp.append(par_k)
        x=plt.boxplot(temp,notch=0, sym='+', vert=1, whis=1.5)

    plt.ylim(0,40)
    plt.xlabel("Term Overlaps")
    plt.ylabel('Parameter = cluster_size')
    #plt.xlim(7,9)
    plt.xticks(range(len(labels)) ,labels,horizontalalignment='center')
    plt.legend( bbox_to_anchor=(1.0, 0.9), loc=1, ncol=1, borderaxespad=0.)
    f1.savefig("para_k_range" + ".png")
