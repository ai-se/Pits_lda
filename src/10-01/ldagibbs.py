from __future__ import print_function, division

__author__ = 'amrit'

from random import randint, random, seed, shuffle, sample
import numpy as np
import os
import lda
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
import copy
import time


def calculate(topics=[], lis=[], count1=0):
    count = 0
    for i in topics:
        if i in lis:
            count += 1
    if count >= count1:
        return count
    else:
        return 0


def recursion(topic=[], index=0, count1=0):
    count = 0
    global data
    # print(data)
    # print(topics)
    d = copy.deepcopy(data)
    d.pop(index)
    for l, m in enumerate(d):
        # print(m)
        for x, y in enumerate(m):
            if calculate(topics=topic, lis=y, count1=count1) != 0:
                count += 1
                break
                # data[index+l+1].pop(x)
    return count


data = []


def jaccard(a, score_topics=[], term=0):
    labels = []  # ,6,7,8,9]
    labels.append(term)
    global data
    l = []
    data = []
    file_data = {}
    for doc in score_topics:
        l.append(doc.split())
    for i in xrange(0, len(l), int(a)):
        l1 = []
        for j in xrange(int(a)):
            l1.append(l[i + j])
        data.append(l1)
    dic = {}
    for x in labels:
        j_score = []
        for i, j in enumerate(data):
            for l, m in enumerate(j):
                sum = recursion(topic=m, index=i, count1=x)
                if sum != 0:
                    j_score.append(sum / float(9))
                '''for m,n in enumerate(l):
                    if n in j[]'''
        dic[x] = j_score
        if len(dic[x]) == 0:
            dic[x] = [0]
    file_data['citemap'] = dic
    X = xrange(len(labels))
    Y_median = []
    Y_iqr = []
    for feature in labels:
        Y = file_data['citemap'][feature]
        Y=sorted(Y)
        return Y[int(len(Y)/2)]


def get_top_words(model, path1, feature_names, n_top_words, i=0, file1=''):
    topics = []
    fo = open(path1,'a+')
    fo.write("Run: " + str(i) + "\n")
    for topic_idx, topic in enumerate(model.components_):
        str1 = ''
        fo.write("Topic " + str(topic_idx) + ": ")
        for j in topic.argsort()[:-n_top_words - 1:-1]:
            str1 += feature_names[j] + " "
            fo.write(feature_names[j] + " ")
        topics.append(str1)
        fo.write("\n")
    fo.close()
    return topics

def _test_LDA(l, path1, file='',data_samples=[],term=0):
    n_topics = 10
    n_top_words = 10

    fileB = []
    fileB.append(file)
    #filepath = '/home/amrit/GITHUB/Pits_lda/dataset/'
    topics=[]
    for j, file1 in enumerate(fileB):
        for i in xrange(10):
            #data_samples = readfile1(filepath + str(file1))

            # shuffling the list
            shuffle(data_samples)

            tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
            tf = tf_vectorizer.fit_transform(data_samples)

            lda1 = lda.LDA(n_topics=int(l[0]), alpha=l[1], eta=l[2],n_iter=200)

            lda1.fit_transform(tf)

            # print("done in %0.3fs." % (time() - t0))
            tf_feature_names = tf_vectorizer.get_feature_names()
            topics.extend(get_top_words(lda1, path1, tf_feature_names, n_top_words, i=i, file1=file1))
    return topics


def main(*x, **r):
    # 1st r
    start_time = time.time()
    base = '/share/aagrawa8/Data/results/'
    path = os.path.join(base, 'topics_gibbs_stability', r['file'], str(r['term']))
    if not os.path.exists(path):
        os.makedirs(path)
    l = np.asarray(x)
    b = int(l[0])
    path1 = path + "/K_" + str(b) + "_a_" + str(l[1]) + "_b_" + str(l[2]) + ".txt"
    with open(path1, "w") as f:
        f.truncate()


    topics = _test_LDA(l, path1, file=r['file'],data_samples=r['data_samples'],term=int(r['term']))
    top=[]
    for i in topics:
        temp=str(i.encode('ascii','ignore'))
        top.append(temp)
    a = jaccard(b, score_topics=top, term=int(r['term']))
    fo = open(path1, 'a+')
    fo.write("\nRuntime: --- %s seconds ---\n" % (time.time() - start_time))
    fo.write("\nScore: " + str(a))
    fo.close()
    return a
