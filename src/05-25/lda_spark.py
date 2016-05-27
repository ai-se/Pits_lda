from __future__ import print_function, division

__author__ = 'amrit'

import os
import sys
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.rdd import RDD
from pyspark.mllib.linalg import Vector, Vectors
from pyspark.mllib.clustering import LDAModel, LDA
from pyspark.ml import Pipeline
from pyspark.sql import Row, SQLContext
from pyspark.sql.types import *
from pyspark.ml.feature import CountVectorizer, CountVectorizerModel, RegexTokenizer


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

def preprocess(sc, path='', vocabsize=5000, stopwordfile=''):
    sqlContext = SQLContext.getOrCreate(sc)
    #import sqlContext.implicits._
    row=Row("docs")

    df = sc.textFile(path).map(row).toDF()
    tokenizer = RegexTokenizer(inputCol="docs", outputCol="rawTokens")
    countVectorizer = CountVectorizer(inputCol="rawTokens", outputCol="features")

    pipeline = Pipeline(stages=[tokenizer,countVectorizer])
    model = pipeline.fit(df)
    documents = model.transform(df).select("features").rdd.map(lambda x: x.features).zipWithIndex().map(lambda x: [x[1], x[0]])
    return documents, model.stages[1].vocabulary #, documents.map(lambda x:x[2].numActives).sum().toLong

if __name__ == '__main__':


    '''conf = SparkConf().setAppName("lda")
    conf.setMaster(sys.argv(1))
    conf.set("spark.executor.memory", "6g")
    conf.set("spark.driver.memory", "6g")
    conf.set("spark.driver.maxResultSize", "6g")
    conf.set("spark.yarn.executor.memoryOverhead", "2g")
    conf.set("spark.yarn.driver.memoryOverhead", "2g")

    conf.set("spark.eventLog.enabled", "true")
    conf.set("spark.eventLog.dir", "hdfs://" + sys.argv(3) + "/user/" + sys.argv(4) + "/Logs/")
    dataset = "hdfs://" + sys.argv(3) + "/user/" + sys.argv(4) + "/In/" + sys.argv(2)'''
    dataset='/home/amrit/GITHUB/Pits_lda/dataset/test'
    sc = SparkContext("local")
    #corpus, vocabArray, actualNumTokens = preprocess(sc, path=dataset, vocabsize=50000, stopwordfile='')
    corpus, vocabArray = preprocess(sc, path=dataset, vocabsize=50000, stopwordfile='')
    corpus.cache()
    actualCorpusSize = corpus.count()
    actualVocabSize = len(vocabArray)
    ##preprocessElapsed = (System.nanoTime() - preprocessStart) / 1e9
