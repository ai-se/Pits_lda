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

    lda1 = lda.LDA(n_topics=10, alpha=0.1, eta=0.01, n_iter=200)
    lda1.fit_transform(tf)
    base = '/share/aagrawa8/Data/results/'
    path = os.path.join(base, 'topics_untuned_stability', res)
    if not os.path.exists(path):
        os.makedirs(path)

    path1 = path + "/K_" + str(int(10)) + "_a_" + str(0.1) + "_b_" + str(0.1) + ".txt"

    #[str,str]
    topics=get_top_words(lda1, path1, tf_feature_names, 10)
    tops = lda1.doc_topic_
    ##from doc_top_distribution
    actual=[]
    for i in xrange(len(data_samples)):
        actual.append(tops[i].argmax())
    predicted=overlap(topics,data_samples)
    actual=np.array(actual)
    predicted=np.array(predicted)
    value=float(np.sum(actual == predicted))/len(actual)
    return value

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

    l=[]
    value={}
    value[res]=call_lda(l,data_samples,res)
    time1={}
    # runtime,format dict, file,=runtime in secs
    time1[res] = time.time() - start_time
    temp=[time1,value]


    with open('dump/topics_untuned_stability_'+res+'.pickle', 'wb') as handle:
        pickle.dump(temp, handle)
    print("\nTotal Score: --- %s %% ---\n" % (value[res]))
    print("\nTotal Runtime: --- %s seconds ---\n" % (time.time() - start_time))


bounds = [(10, 30), (0.1, 1), (0.1, 1)]
max_fitness = 0
if __name__ == '__main__':
    eval(cmd())
