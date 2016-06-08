from __future__ import print_function, division

__author__ = 'amrit'

import sys
import pickle
from demos import atom
from demos import cmd
import collections
from ldamodel import *
import random
import time
import copy
import operator
import matplotlib.pyplot as plt
import os, pickle

__all__ = ['DE']
Individual = collections.namedtuple('Individual', 'ind fit')


class DE(object):
    def __init__(self, x='rand', y=1, z='bin', F=0.3, CR=0.7):
        self.x = x
        self.y = y
        self.z = z
        self.F = F
        self.CR = CR

    # TODO: add a fitness_aim param?
    # TODO: add a generic way to generate initial pop?
    def solve(self, fitness, initial_population, iterations=10, **r):
        current_generation = [Individual(ind, fitness(*ind, **r)) for ind in
                              initial_population]
        dic={}
        for i in current_generation:
            if i.fit in dic.keys():
                dic[i.fit].append(i.ind)
            else:
                dic[i.fit]=[i.ind]
        for _ in range(iterations):
            trial_generation = []

            for ind in current_generation:
                v = self._extrapolate(ind,current_generation)
                trial_generation.append(Individual(v, fitness(*v, **r)))

            for x in trial_generation:
                if x.fit in dic.keys():
                    dic[x.fit].append(x.ind)
                else:
                    dic[x.fit]=[x.ind]

            current_generation = self._selection(current_generation,
                                                 trial_generation)

        best_index = self._get_best_index(current_generation)
        return current_generation[best_index].ind, current_generation[best_index].fit, dic

    def select3others(self,population):
        popu=copy.deepcopy(population)
        x= random.randint(0, len(popu)-1)
        x1=popu[x]
        popu.pop(x)
        y= random.randint(0, len(popu)-1)
        y1=popu[y]
        popu.pop(y)
        z= random.randint(0, len(popu)-1)
        z1=popu[z]
        popu.pop(z)
        return x1.ind,y1.ind,z1.ind

    def _extrapolate(self, ind, population):
        if (random.random() < self.CR):
            x,y,z=self.select3others(population)
            #print(x,y,z)
            mutated=[x[0] + self.F*(y[0] - z[0]), x[1] + self.F*(y[1] - z[1]), x[2] + self.F*(y[2] - z[2])]

            check_mutated= [max(bounds[0][0], min(mutated[0], bounds[0][1])),max(bounds[1][0], min(mutated[1], bounds[1][1])) ,max(bounds[2][0], min(mutated[2], bounds[2][1]))]
            return check_mutated
        else:
            return ind.ind

    def _selection(self, current_generation, trial_generation):
        generation = []

        for a, b in zip(current_generation, trial_generation):
            if a.fit >= b.fit:
                generation.append(a)
            else:
                generation.append(b)

        return generation

    def _get_indices(self, n, upto, but=None):
        candidates = list(range(upto))

        if but is not None:
            # yeah O(n) but random.sample cannot use a set
            candidates.remove(but)

        return random.sample(candidates, n)

    def _get_best_index(self, population):
        global max_fitness
        best = 0

        for i, x in enumerate(population):
            if x.fit >= max_fitness:
                best = i
                max_fitness = x.fit
        return best

    def _set_x(self, x):
        if x not in ['rand', 'best']:
            raise ValueError("x should be either 'rand' or 'best'.")

        self._x = x

    def _set_y(self, y):
        if y < 1:
            raise ValueError('y should be > 0.')

        self._y = y

    def _set_z(self, z):
        if z != 'bin':
            raise ValueError("z should be 'bin'.")

        self._z = z

    def _set_F(self, F):
        if not 0 <= F <= 2:
            raise ValueError('F should belong to [0, 2].')

        self._F = F

    def _set_CR(self, CR):
        if not 0 <= CR <= 1:
            raise ValueError('CR should belong to [0, 1].')

        self._CR = CR

    x = property(lambda self: self._x, _set_x, doc='How to choose the vector '
                                                   'to be mutated.')
    y = property(lambda self: self._y, _set_y, doc='The number of difference '
                                                   'vectors used.')
    z = property(lambda self: self._z, _set_z, doc='Crossover scheme.')
    F = property(lambda self: self._F, _set_F, doc='Weight used during '
                                                   'mutation.')
    CR = property(lambda self: self._CR, _set_CR, doc='Weight used during '
                                                      'bin crossover.')


def cmd(com="demo('-h')"):
    "Convert command line to a function call."
    if len(sys.argv) < 2: return com

    def strp(x): return isinstance(x, basestring)

    def wrap(x): return "'%s'" % x if strp(x) else str(x)

    words = map(wrap, map(atom, sys.argv[2:]))
    return sys.argv[1] + '(' + ','.join(words) + ')'



def _test(res=''):
    start_time = time.time()
    labels = [8,9]
    random.seed(1)
    global bounds
    result = {}
    a={}
    score1={}
    temp2={}
    for lab in labels:
        global max_fitness
        max_fitness = 0
        print(res+'\t'+str(lab))

        if res == 'F3CR7pop10':
            de = DE(F=0.3, CR=0.7, x='rand')
            pop = [[random.randint(bounds[0][0], bounds[0][1]), random.uniform(bounds[1][0], bounds[1][1]),
                    random.uniform(bounds[2][0], bounds[2][1])]
                   for _ in range(10)]  # 20 * dimension of the problem
        elif res == 'F7CR3pop10':
            de = DE(F=0.7, CR=0.3, x='rand')
            pop = [[random.randint(bounds[0][0], bounds[0][1]), random.uniform(bounds[1][0], bounds[1][1]),
                    random.uniform(bounds[2][0], bounds[2][1])]
                   for _ in range(10)]
        elif res == 'F7CR3pop30':
            de = DE(F=0.7, CR=0.3, x='rand')
            pop = [[random.randint(bounds[0][0], bounds[0][1]), random.uniform(bounds[1][0], bounds[1][1]),
                    random.uniform(bounds[2][0], bounds[2][1])]
                   for _ in range(30)]
        elif res == 'F3CR7pop30':
            de = DE(F=0.3, CR=0.7, x='rand')
            pop = [[random.randint(bounds[0][0], bounds[0][1]), random.uniform(bounds[1][0], bounds[1][1]),
                    random.uniform(bounds[2][0], bounds[2][1])]
                   for _ in range(30)]
        z={}
        temp={}
        for i in range(1,5):
            v, score,temp[i] = de.solve(main, pop, iterations=i, file='101pitsA_2.txt', term=lab, res=res)
            z[i]=score
            print(v, '->', score)
        a[lab]=z
        score1[lab]=temp
        temp2[lab]= max(a[lab].iteritems(), key=operator.itemgetter(1))[1]
    result[res] = temp2
    print(result)
    print(a)
    print(score1)

    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 20}

    plt.rc('font', **font)
    paras={'lines.linewidth': 5,'legend.fontsize': 20, 'axes.labelsize': 30, 'legend.frameon': False,'figure.autolayout': True,'figure.figsize': (16,8)}
    plt.rcParams.update(paras)
    X = range(len(labels))
    plt.figure(num=0, figsize=(25, 15))
    labels=[5,6,8,9]
    a[5]={1: 0.8, 2: 0.8, 3: 0.9, 4: 0.9}
    a[6]={1: 0.7, 2: 0.7, 3: 0.7, 4: 0.8}
    #plt.subplot(121)
    for lab in labels:
        Y_tuned=[]
        Y_untuned=[]
        Y_final=[]
        for l in range(1,4):
            Y_tuned.append(a[lab][l])
        line, = plt.plot(X, Y_tuned, marker='o', markersize=16, label='term_overlap='+str(lab))
    plt.xticks(X, range(100,500,100))
    plt.ylabel("Stability score")
    plt.xlabel("No of evaluations")
    plt.legend(bbox_to_anchor=(0.95, 0.5), loc=1, ncol = 1, borderaxespad=0.)
    plt.savefig("tuned_pitsA" + ".png")
    '''
    plt.figure(num=1, figsize=(25, 15))
    labels=[5,6,8,9]
    a[5]={1: 0.8, 2: 0.8, 3: 0.9, 4: 0.9}
    a[6]={1: 0.7, 2: 0.7, 3: 0.7, 4: 0.8}
    #plt.subplot(121)
    for lab in labels:
        Y_tuned=[]
        Y_untuned=[]
        Y_final=[]
        for l in range(1,4):
            score1[lab][l]
            Y_tuned.append(a[lab][l])
        line, = plt.plot(X, Y_tuned, marker='o', markersize=16, label='term_overlap='+str(lab))
    plt.xticks(X, range(100,400,100))
    plt.ylabel("Stability score")
    plt.xlabel("No of evaluations")
    plt.legend(bbox_to_anchor=(0.95, 0.5), loc=1, ncol = 1, borderaxespad=0.)
    plt.savefig("tuned_pitsA" + ".png")'''

    with open('dump/pitsA_'+res+'.pickle', 'wb') as handle:
        pickle.dump(result, handle)
        pickle.dump(score1, handle)
        pickle.dump(a, handle)
    print("\nTotal Runtime: --- %s seconds ---\n" % (time.time() - start_time))
'''
F7CR3pop10      5
[26, 0.0021060533511106927, 0.4453871940548014] -> 0.8
[14, 0.43788759365057206, 0.49581224138185065] -> 0.8
[27.3, 1, 0.4265773971277693] -> 0.9
[28.7, 0.8038011147599253, 1] -> 0.9

[12, 0.8474337369372327, 0.763774618976614] -> 0.8
[18.4, 0.5417577383577451, 0.7242095524410068] -> 0.8
[12, 0.8474337369372327, 0.763774618976614] -> 0.8
[12, 0.8474337369372327, 0.763774618976614] -> 0.7
[12, 0.8474337369372327, 0.763774618976614] -> 0.8
F7CR3pop10      6
[24, 0.739895460338587, 0.8564663413124556] -> 0.7
[30, 0.6355740082311631, 0.0235501678432124] -> 0.7
[30, 1, 0] -> 0.7
[23.9, 0.9913334972382413, 0.43743418937404754] -> 0.8
[30, 0.971080954988909, 0] -> 0.8
[26.0, 1, 0.3376198279346765] -> 0.8
[30, 1, 0.09171616479838399] -> 0.8
[30, 1, 0] -> 0.8
[30, 1, 0.34437784210719147] -> 0.8'''

bounds = [(10, 30), (0, 1), (0, 1)]
max_fitness = 0
if __name__ == '__main__':
    eval(cmd())
