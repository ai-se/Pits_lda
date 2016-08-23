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
    for i in range(0, len(l), int(a)):
        l1 = []
        for j in range(int(a)):
            l1.append(l[i + j])
        data.append(l1)
    dic = {}
    for x in labels:
        j_score = []
        for i, j in enumerate(data):
            for l, m in enumerate(j):
                sum = recursion(topic=m, index=i, count1=x)
                if sum != 0:
                    j_score.append(sum / float(3))
                '''for m,n in enumerate(l):
                    if n in j[]'''
        dic[x] = j_score
        if len(dic[x]) == 0:
            dic[x] = [0]
    file_data['citemap'] = dic
    X = range(len(labels))
    Y_median = []
    Y_iqr = []
    for feature in labels:
        Y = file_data['citemap'][feature]
        Y=sorted(Y)
        return Y[int(len(Y)/2)]

test = ["glori telemetri command spacecraft trace smrd tim spec pip parent",
         "spec smrd parent child glori artifact referenc verif matrix data",
         "test case accuraci roll document glori plan pitch yaw valu",
         "command specifi ground softwar telemetri initi pip data configur band",
        "command specifi ground softwar initi telemetri data pip configur band",
         "document test glori initi plan roll case pitch yaw point",
         "spec smrd parent child glori artifact verif point matrix spacecraft",
         "pip capabl glori ground command smrd spec tim list spacecraft",
        "spec smrd parent child glori referenc artifact verif matrix spacecraft",
         "command telemetripip ground spacecraft modesoftwar document spec glori",
         "command specifi ground softwar initi telemetri data configur pip band",
         "test initi accuraci glori roll plan matrix yaw pitch valu",
        "command specifi tim pip ground telemetri glori includ softwar document",
         "test initi glori plan roll accuraci case pip point yaw",
         "command specifi ground softwar telemetri initi data pip configur band",
         "spec smrd child glori artifact referenc parent verif matrix data"]

for lab in range(1,10):
    a = jaccard(4, score_topics=test, term=lab)
    print a

