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
import matplotlib.pyplot as plt
import os, pickle

def _test(res=''):
    #fileB = ['pitsA', 'pitsB', 'pitsC', 'pitsD', 'pitsE', 'pitsF', 'processed_citemap.txt']
    #fileB = ['SE0.txt', 'SE6.txt', 'SE1.txt', 'SE8.txt', 'SE3.txt']
    filepath = '/home/amrit/GITHUB/Pits_lda/dataset/'


    data_samples = readfile1(filepath + str(res))
    labels = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    #labels = [7,50,100,200,400]
    start_time = time.time()
    random.seed(1)
    global bounds
    # stability score format dict, file,lab=score
    result={}
    # parameter variations (k,a,b), format, dict, file,lab,each score=k,a,b
    final_para_dic={}
    temp1={}
    temp3={}

    for lab in labels:
        global max_fitness
        max_fitness = 0
        dic={}
        v=[]
        print(res+'\t'+str(lab))
        for i in range(30):
            l=[randint(10,30),random.uniform(0.01,1),random.uniform(0.01,1)]
            score=main(l,file=res, term=lab, data_samples=data_samples)
            if score>=max_fitness:
                max_fitness=score
                v=l
            if score in dic.keys():
                dic[score].append(l)
            else:
                dic[score]=[l]

        temp1[lab]=dic

        print(v, '->', max_fitness)

        temp3[lab]= max_fitness
    result[res] = temp3
    final_para_dic[res]=temp1

    print(result)
    print(final_para_dic)
    time1={}
    # runtime,format dict, file,=runtime in secs
    time1[res]=time.time() - start_time
    l=[result,final_para_dic,time1]

    with open('dump/random_gibbs'+res+'.pickle', 'wb') as handle:
        pickle.dump(l, handle)
    print("\nTotal Runtime: --- %s seconds ---\n" % (time.time() - start_time))


bounds = [(10, 30), (0.1, 1), (0.1, 1)]
max_fitness = 0
if __name__ == '__main__':
    eval(cmd())
