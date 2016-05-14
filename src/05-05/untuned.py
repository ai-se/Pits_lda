from __future__ import print_function, division

__author__ = 'amrit'

from random import randint, random, seed, shuffle, sample
from time import time
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from collections import Counter
import copy
import numpy as np
import random

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

def jaccard(a,file='',term=0):
    fileB = []#, '101pitsB_2.txt', '101pitsC_2.txt','101pitsD_2.txt','101pitsE_2.txt','101pitsF_2.txt']
    fileB.append(file)
    labels=[]#,6,7,8,9]
    labels.append(term)
    global data
    l=[]
    data=[]
    file_data={}
    for file1 in fileB:
        with open("../../results/05-05/shuffle_"+file1, 'r') as f:
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
            return np.median(Y)


def get_top_words(model, feature_names, n_top_words, i=0,file1=''):
    filepath = "../../results/05-05/shuffle_"+file1
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

def _test_LDA(l,file=''):
    n_topics = 10
    n_top_words = 10

    fileB = []
    fileB.append(file)

    filepath = "../../dataset/"

    for j, file1 in enumerate(fileB):
        filepath1 = "../../results/05-05/shuffle_"+file1
        with open(filepath1,"w") as f:
            f.truncate()
        for i in range(10):
            data_samples = readfile1(filepath + str(file1))

            # shuffling the list
            shuffle(data_samples)

            tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
            tf = tf_vectorizer.fit_transform(data_samples)

            lda = LatentDirichletAllocation(n_topics=int(l[0]), learning_method='online',
                 learning_decay=0.7, learning_offset=50., max_iter=10)
            t0 = time()
            tf_new = lda.fit_transform(tf)

            #print("done in %0.3fs." % (time() - t0))
            tf_feature_names = tf_vectorizer.get_feature_names()
            get_top_words(lda, tf_feature_names, n_top_words,i,file1)

def main():
    # 1st r
    fileB = ['101pitsA_2.txt', '101pitsB_2.txt', '101pitsC_2.txt','101pitsD_2.txt','101pitsE_2.txt', '101pitsF_2.txt']
    labels=[1,2,3,4, 5 ,6,7,8,9]
    l=[10]
    result={}
    for file1 in fileB:
        file_result={}
	for terms in labels:
	    print(file1, '\t', terms)
	    _test_LDA(l,file=file1)

	    # 2nd method
	    #another_method()
	    file_result[terms] = jaccard(int(l[0]),file=file1, term=terms)
	result[file1]=file_result
    print(result)

main()
