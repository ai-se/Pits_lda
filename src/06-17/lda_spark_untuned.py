from __future__ import print_function, division

__author__ = 'amrit'

import os
import sys
import pickle
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
    X = range(len(labels))
    Y_median = []
    Y_iqr = []
    for feature in labels:
        Y = file_data['abc'][feature]
        Y=sorted(Y)
        return Y[int(len(Y)/2)]


def preprocess(sc, path='', vocabsize=5000, stopwordfile=''):
    sqlContext = SQLContext.getOrCreate(sc)
    row = Row("docs")
    #shuffle(row)
    df = sc.textFile(path).map(row).toDF()
    tokenizer = RegexTokenizer(inputCol="docs", outputCol="rawTokens")
    countVectorizer = CountVectorizer(inputCol="rawTokens", outputCol="features")

    pipeline = Pipeline(stages=[tokenizer, countVectorizer])
    model = pipeline.fit(df)
    documents = model.transform(df).select("features").rdd.map(lambda x: x.features).zipWithIndex().map(
        lambda x: [x[1], x[0]])
    return documents, model.stages[1].vocabulary


if __name__ == '__main__':
    start_time1 = time.time()
    args = sys.argv
    sconf = SparkConf()
    sconf.setAppName("lda")
    sconf.setMaster(args[1])
    sconf.set("spark.executor.memory", "6g")
    sconf.set("spark.driver.memory", "6g")
    sconf.set("spark.driver.maxResultSize", "6g")
    sconf.set("spark.yarn.executor.memoryOverhead", "2g")
    sconf.set("spark.yarn.driver.memoryOverhead", "2g")

    sconf.set("spark.eventLog.enabled", "true")
    sconf.set("spark.eventLog.dir", "hdfs://" + args[3] + "/user/" + args[4] + "/Logs/")
    sc = SparkContext(conf=sconf)
    dataset = "hdfs://" + args[3] + "/user/" + args[4] + "/In/" + args[2]
    corpus, vocabArray = preprocess(sc, path=dataset, vocabsize=50000, stopwordfile='')

    base = os.path.abspath(os.path.dirname(__file__))
    result={}
    #l=list(range(corpus.count()))

    temp={}
    for lab in range(1,10):
        median1=[]
        path = os.path.join(base,'untuned',args[2] , str(lab))
        start_time = time.time()
        if not os.path.exists(path):
            os.makedirs(path)
        for j in range(10):
                start_time = time.time()
                path1 = path + "/run_" + str(j) + ".txt"
                with open(path1, "w") as f:
                    f.truncate()

                with open(path1,"w") as f:
                        f.truncate()
                fo = open(path1, 'w+')
                score_topic = []
                for i in range(10):
                    fo.write("Run : " + str(i) + "\n")

                    ''''shuffle(l)
                    x=sc.parallelize(l).map(lambda d:(d,0))
                    corpus = corpus.map(lambda e: (e[0],e[1]))
                    print(x.collect())
                    corpus=corpus.join(x).map(lambda e: [e[0],e[1][0]] )'''

                    x=corpus.collect()
                    shuffle(x)
                    corpus=sc.parallelize(x)
                    ldaModel = LDA.train(corpus, k=10, maxIterations=20, docConcentration=-1.0, topicConcentration=-1.0, checkpointInterval=10, optimizer='online')
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
                b = jaccard(10, tops=score_topic, term=lab)
                fo.write("\nRuntime: --- %s seconds ---\n" % (time.time() - start_time))
                fo.write("\nScore: "+str(b))
                median1.append(b)
                fo.close()
        temp[lab]=median1
    result[args[2]]=temp
    print(result)
    time1={}
    # runtime,format dict, file,=runtime in secs
    time1[args[2]]=time.time() - start_time1
    print("\nRuntime: --- %s seconds ---\n" % (time.time() - start_time1))
    with open('dump/untuned'+args[2]+'.pickle', 'wb') as handle:
        pickle.dump(result, handle)
        pickle.dump(time1,handle)
    sc.stop()
