from __future__ import print_function, division

__author__ = 'amritanshu.agrawal'

import sys

sys.dont_write_bytecode = True
import collections
import random
from demos import cmd
from ldagibbs import *
import time
import pickle

__all__ = ['DE']
Individual = collections.namedtuple('Individual', 'ind fit')

class GA(object):
    def __init__(self, F=0.01, CR=0.6, Elite=2, early=10, terminate=100):
        self.F = F
        self.CR = CR
        self.E=Elite
        self.T=terminate
        self.ET=early
        if self.ET > self.T:
            print("Error: Early termination is more than Termination Value. Forcing Early termination to Termination value")
            self.ET=self.T

    # TODO: add a fitness_aim param?
    # TODO: add a generic way to generate initial pop?
    def solve(self, fitness, initial_population, **r):
        current_generation = [Individual(ind, fitness(*ind, **r)) for ind in
                              initial_population]
        termination=1
        for _ in range(self.T):

            trial_generation = []
            temp_generation=[]
            indices = self._get_best_indices(current_generation, self.E)
            for i in indices:
                temp_generation.append(Individual(current_generation[i].ind, current_generation[i].fit))
            current_generation = [i for j, i in enumerate(current_generation) if j not in indices]

            if set(indices) == set(range(len(indices))):
                termination+=1
                if termination==self.ET:
                    break
            else:
                termination=1

            for i,ind in enumerate(current_generation):
                v,flag = self._extrapolate(current_generation[i])
                if flag:
                    trial_generation.append(Individual(v, fitness(*v, **r)))
                else:
                    trial_generation.append(Individual(v.ind, v.fit))

            current_generation = temp_generation+self._selection(current_generation,trial_generation)

        best_index = self._get_best_indices(current_generation, 1)
        return current_generation[best_index[0]].ind, current_generation[best_index[0]].fit

    def _extrapolate(self, chrome):
        flag=True
        if (random.random() < self.CR):
            x=chrome.ind
            if (random.random() < self.CR):
                mutated = [x[0] + 1, x[1] + 0.01, x[2] + 0.01]
            else:
                mutated = [x[0] - 1, x[1] - 0.01, x[2] - 0.01]
            check_mutated= [max(bounds[0][0], min(mutated[0], bounds[0][1])),max(bounds[1][0], min(mutated[1], bounds[1][1])) ,max(bounds[2][0], min(mutated[2], bounds[2][1]))]
            return check_mutated, flag
        else:
            flag=False
            return chrome, flag

    def _selection(self, current_generation, trial_generation):
        generation = []

        for a, b in zip(current_generation, trial_generation):
            if a.fit <= b.fit:
                generation.append(a)
            else:
                generation.append(b)

        return generation

    def _get_best_indices(self, population, E):
        import heapq
        return heapq.nlargest(E, xrange(len(population)), key=population.__getitem__)

def readfile1(filename=''):
    dict = []
    with open(filename, 'r') as f:
        for doc in f.readlines():
            try:
                row = doc.lower().strip()
                dict.append(row)
            except:
                pass
    return dict

def _test(res=''):
    filepath = '/share/aagrawa8/Data/Pits/'
    random.seed(1)
    np.random.seed(1)
    start_time = time.time()
    #filepath='/Users/amrit/GITHUB/Pits_lda/dataset/'
    data_samples = readfile1(filepath + str(res)+'.txt')

    ga = GA(F=0.01, CR=0.6, Elite=2, early=10, terminate=100)
    pop = [[random.randint(bounds[0][0], bounds[0][1]), random.uniform(bounds[1][0], bounds[1][1]),
            random.uniform(bounds[2][0], bounds[2][1])]
           for _ in range(100)]
    params,fit = ga.solve(main, pop, data_samples=data_samples)

    labels = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    temp={}
    final={}
    for lab in labels:
        a = main_another(params, file=res, term=lab, data_samples=data_samples)
        temp[lab] = a
        #temp[lab]=[params,fit,a]
    endtime=time.time() - start_time
    final[res] = [params, fit, endtime, temp]
    #final[res]=[temp, endtime]
    print(final)
    with open('dump/'+res+'.pickle','wb') as handle:
        pickle.dump(final, handle)

bounds = [(10, 30), (0.1, 1), (0.1, 1)]

if __name__ == '__main__':
    eval(cmd())