from __future__ import print_function, division

__author__ = 'amrit'

from demos import atom
import sys
import lda.utils
import lda.datasets
from random import randint, random, seed, shuffle, sample
from time import time
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from collections import Counter
import copy
import numpy as np
import matplotlib.pyplot as plt

def calculate(topics=[], lis=[], count1=0):
    count=0
    for i in topics:
        if i in lis:
            count+=1
    if count>=count1:
        return count
    else:
        return 0

def recursion(topic=[], index=0, count1=0):
    count=0
    global data
    #print(data)
    #print(topics)
    d=copy.deepcopy(data)
    d.pop(index)
    for l,m in enumerate(d):
        #print(m)
        for x,y in enumerate(m):
            if calculate(topics=topic,lis=y,count1=count1) !=0 :
                count+=1
                break
                #data[index+l+1].pop(x)
    return count

data=[]

def jaccard(a):
    fileB = ['101pitsA_2.txt']#, '101pitsB_2.txt', '101pitsC_2.txt','101pitsD_2.txt','101pitsE_2.txt','101pitsF_2.txt']
    labels=[5]#,6,7,8,9]
    global data
    l=[]
    data=[]
    file_data={}
    for file1 in fileB:
        with open("../../results/04-21/shuffled_"+file1, 'r') as f:
            for doc in f.readlines():
                l.append(doc.split())
            # print(len(l))
            #for i in range(len(l)-(int(a)+1),-1,-(int(a)+1)):
            #     l.pop(i)
        for i in range (0,len(l),int(a)):
            l1=[]
            for j in range(int(a)):
                l1.append(l[i+j])
            data.append(l1)
        dic={}
        for x in labels:
            j_score=[]
            for i,j in enumerate(data):
                for l,m in enumerate(j):
                    sum=recursion(topic=m, index=i,count1=x)
                    if sum !=0:
                        j_score.append(sum/float(10))
                    '''for m,n in enumerate(l):
                        if n in j[]'''
            dic[x]=j_score
            if len(dic[x])==0:
                dic[x]=[0]
        file_data[file1]=dic
    #print(file_data)
    X=range(len(labels))
    for file1 in fileB:
        Y_median=[]
        Y_iqr=[]
        for feature in labels:
            Y=file_data[file1][feature]
            print("Score: ",np.median(Y))
            return np.median(Y)


def get_top_words(model, feature_names, n_top_words, i=0,file1=''):
    filepath = "../../results/04-21/shuffled_"+file1
    with open(filepath,"a+") as f:
        for topic_idx, topic in enumerate(model.components_):
            for i in topic.argsort()[:-n_top_words - 1:-1]:
                f.write(feature_names[i]+ " ")
            f.write("\n")

def token_freqs(doc):
    return Counter(doc)


def tf(corpus):
    mat = [token_freqs(doc) for doc in corpus]
    return mat


def make_feature(corpus, n_features=1000):
    label = list(zip(*corpus)[0])
    mat = tf(corpus)
    #matt = hash(mat)
    return mat

def cmd(com="demo('-h')"):
    "Convert command line to a function call."
    if len(sys.argv) < 2: return com

    def strp(x): return isinstance(x, basestring)

    def wrap(x): return "'%s'" % x if strp(x) else str(x)

    words = map(wrap, map(atom, sys.argv[2:]))
    return sys.argv[1] + '(' + ','.join(words) + ')'


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

def _test_LDA(l):
    n_topics = 10
    n_top_words = 10

    fileB = ['101pitsA_2.txt']#, '101pitsB_2.txt', '101pitsC_2.txt','101pitsD_2.txt','101pitsE_2.txt', '101pitsF_2.txt']

    filepath = "../../dataset/"

    for j, file1 in enumerate(fileB):
        filepath1 = "../../results/04-21/shuffled_"+file1
        with open(filepath1,"w") as f:
            f.truncate()
        for i in range(10):
            data_samples = readfile1(filepath + str(file1))

            # shuffling the list
            shuffle(data_samples)

            tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
            tf = tf_vectorizer.fit_transform(data_samples)

            lda = LatentDirichletAllocation(n_topics=10, doc_topic_prior=l[0],
                 topic_word_prior=l[1], learning_method='online',
                 learning_decay=l[2], learning_offset=50., max_iter=10,
                 random_state=None)
            t0 = time()
            tf_new = lda.fit_transform(tf)

            #print("done in %0.3fs." % (time() - t0))
            tf_feature_names = tf_vectorizer.get_feature_names()
            get_top_words(lda, tf_feature_names, n_top_words,i,file1)

def main(x):
    # 1st method
    l=np.asarray(x)
    print(l)

    _test_LDA(l)

    # 2nd method
    #another_method()
    jaccard(10)