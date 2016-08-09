from __future__ import print_function, division

__author__ = 'amrit'

import os
import sys
from pyspark import SparkContext
from pyspark import SparkConf
import numpy as np
from random import shuffle
from pyspark.rdd import RDD
from pyspark.mllib.linalg import Vector, Vectors
from pyspark.mllib.clustering import LDAModel, LDA
from pyspark.ml import Pipeline
from pyspark.sql import Row, SQLContext
from pyspark.sql.types import *
from pyspark.ml.feature import CountVectorizer, RegexTokenizer
import time
import copy


# Path for spark source folder
# os.environ['SPARK_HOME'] = "/home/amrit/spark"
#
# # Append pyspark  to Python Path
# sys.path.append("/home/amrit/spark/python")
#
# try:
#     from pyspark import SparkContext
#     from pyspark import SparkConf
#
#     print ("Successfully imported Spark Modules")
#
# except ImportError as e:
#     print ("Can not import Spark Modules", e)
#     sys.exit(1)
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


def jaccard(a, tops=[], term=0):
    labels = []  # ,6,7,8,9]
    labels.append(term)
    global data
    l = []
    data = []
    file_data = {}
    for doc in tops:
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
                    j_score.append(sum / float(9))
                '''for m,n in enumerate(l):
                    if n in j[]'''
        dic[x] = j_score
        if len(dic[x]) == 0:
            dic[x] = [0]
    file_data['abc'] = dic


# print(file_data)
    Y = file_data['abc'][term]
    return np.median(Y)


def preprocess(sc, path='', vocabsize=5000, stopwordfile=''):
    sqlContext = SQLContext.getOrCreate(sc)
    row = Row("docs")
    df = sc.textFile(path).map(row).toDF()
    tokenizer = RegexTokenizer(inputCol="docs", outputCol="rawTokens")
    countVectorizer = CountVectorizer(inputCol="rawTokens", outputCol="features")

    pipeline = Pipeline(stages=[tokenizer, countVectorizer])
    model = pipeline.fit(df)
    documents = model.transform(df).select("features").rdd.map(lambda x: x.features).zipWithIndex().map(
        lambda x: [x[1], x[0]])
    return documents, model.stages[1].vocabulary


def main(*x, **r):
    l = x
    dataset = "hdfs://" + r['ip'] + "/user/" + r['user'] + "/In/" + r['file']
    sc=r['sprkcontext']

    base = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(base,'tuned',r['file'], str(r['label']))
    start_time = time.time()
    if not os.path.exists(path):
        os.makedirs(path)
    b = int(l[0])
    path1 = path + "/K_" + str(b) + "_a_" + str(l[1]) + "_b_" + str(l[2]) + ".txt"
    with open(path1,"w") as f:
            f.truncate()
    fo = open(path1, 'w+')
    score_topic = []
    corpus, vocabArray = preprocess(sc, path=dataset, vocabsize=50000, stopwordfile='')
    #corpus.cache()
    for i in range(10):
        fo.write("Run : " + str(i) + "\n")

        x=corpus.collect()
        shuffle(x)
        corpus=sc.parallelize(x)
        #corpus.cache()
        ldaModel = LDA.train(corpus, k=int(l[0]), maxIterations=20, docConcentration=float(l[1]), topicConcentration=float(l[1]), checkpointInterval=10,
                              optimizer='online')
        # println(s"\t $distLDAModel.topicsMatrix().toArray()")
        topicIndices = ldaModel.describeTopics(maxTermsPerTopic=10)
        topics = []
        for x in topicIndices:
            topics.append(zip(list(map(lambda a: str(vocabArray[int(a)]), x[0])), x[1]))
        for a in range(len(topics)):
            fo.write("Topic " + str(a) + ": ")
            str1 = ''
            for b in topics[a]:
                str1 += b[0] + " "
                fo.write(b[0] + " ")
            score_topic.append(str1)
            fo.write("\n")
        fo.write("\n")
    b = jaccard(int(l[0]), tops=score_topic, term=r['label'])
    fo.write("\nRuntime: --- %s seconds ---\n" % (time.time() - start_time))
    fo.write("\nScore: "+str(b))
    fo.close()
    corpus.unpersist()
    return b
