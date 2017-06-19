from __future__ import print_function, division

__author__ = 'amrit'

import sys
import pickle
from demos import atom
from demos import cmd
import collections
from ldagibbs import *
import random
import time
import copy
import operator
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
        for _ in xrange(iterations):
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
        return current_generation[best_index].ind, current_generation[best_index].fit, dic, current_generation

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
        candidates = list(xrange(upto))

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

def readfile1(filename=''):
    dict = []
    with open(filename, 'r') as f:
        for doc in f.readlines():
            try:
                row = doc.lower().split('>>>')[0].strip()
                dict.append(row)
            except:
                pass
    return dict

def call_lda(l,data_samples,res):
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
    tf = tf_vectorizer.fit_transform(data_samples)
    tf_feature_names = tf_vectorizer.get_feature_names()
    max=0
    for i in l:
        lda1 = lda.LDA(n_topics=int(i[0]), alpha=i[1], eta=i[2], n_iter=200)
        lda1.fit_transform(tf)
        base = '/share/aagrawa8/Data/results/'
        path = os.path.join(base, 'topics_gibbs_stability', res)
        if not os.path.exists(path):
            os.makedirs(path)

        path1 = path + "/K_" + str(int(i[0])) + "_a_" + str(i[1]) + "_b_" + str(i[2]) + ".txt"

        #[str,str]
        topics=get_top_words(lda1, path1, tf_feature_names, 7)
        tops = lda1.doc_topic_
        ##from doc_top_distribution
        actual=[]
        for j in xrange(len(data_samples)):
            actual.append(tops[j].argmax())
        predicted=overlap(topics,data_samples)
        actual=np.array(actual)
        predicted=np.array(predicted)
        value=float(np.sum(actual == predicted))/len(actual)
        if value >=max:
            max=value
    return max

def overlap(topics, data_samples):
    predicted = []
    for i in data_samples:
        l=[]
        for x in topics:
            count=0
            for y in x.split():
                if y in i.split():
                    count+=1
            l.append(count)
        predicted.append(np.array(l).argmax())
    return predicted



def _test(res=''):
    #fileB = ['pitsA', 'pitsB', 'pitsC', 'pitsD', 'pitsE', 'pitsF', 'processed_citemap.txt']
    #fileB = ['SE0.txt', 'SE6.txt', 'SE1.txt', 'SE8.txt', 'SE3.txt']
    filepath = '/share/aagrawa8/Data/'

    #[str,str]
    data_samples = readfile1(filepath + str(res))
    #labels = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    #labels = [7,50,100,200]
    labels=[7]
    start_time = time.time()
    random.seed(1)
    global bounds
    # stability score format dict, file,lab=score
    result={}
    # parameter variations (k,a,b), format, dict, file,lab,each score=k,a,b
    final_para_dic={}
    # final generation, format dict, file,lab=parameter, score
    final_current_dic={}
    de = DE(F=0.7, CR=0.3, x='rand')
    temp1={}
    temp2={}
    temp3={}
    for lab in labels:
        global max_fitness
        max_fitness = 0
        print(res+'\t'+str(lab))
        pop = [[random.randint(bounds[0][0], bounds[0][1]), random.uniform(bounds[1][0], bounds[1][1]),
                    random.uniform(bounds[2][0], bounds[2][1])]
                   for _ in xrange(10)]
        v, score,para_dict,gen = de.solve(main, pop, iterations=3, file=res, term=lab, data_samples=data_samples)
        temp1[lab]=para_dict
        temp2[lab]=gen
        print(v, '->', score)

        temp3[lab]= score
    result[res] = temp3
    final_para_dic[res]=temp1
    final_current_dic[res]=temp2
    print(result)
    print(final_current_dic)
    print(final_para_dic)
    time1={}

    l = final_para_dic[res][7][result[res][7]]
    print(l)
    value={}
    value[res]=call_lda(l,data_samples,res)

    # runtime,format dict, file,=runtime in secs
    time1[res] = time.time() - start_time
    temp=[result,final_para_dic,time1,value]


    with open('dump/topics_gibbs_stability_'+res+'.pickle', 'wb') as handle:
        pickle.dump(temp, handle)
    print("\nTotal Score: --- %s ---\n" % (value[res]))
    print("\nTotal Runtime: --- %s seconds ---\n" % (time.time() - start_time))


bounds = [(10, 30), (0.1, 1), (0.1, 1)]
max_fitness = 0
if __name__ == '__main__':
    eval(cmd())