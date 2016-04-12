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
import numpy as np


def get_top_words(model, feature_names, n_top_words, i=0):
    filepath = "../../results/04-11/result.txt"
    with open(filepath,"a+") as f:
        f.write("Run "+str(i)+" :\n")
        for topic_idx, topic in enumerate(model.components_):
            # print("Topic #%d:" % topic_idx)
            for i in topic.argsort()[:-n_top_words - 1:-1]:
                f.write(feature_names[i]+ " ")
            f.write("\n")
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


def readfile1(filename='', thres=[0.0, 0.1]):
    dict = []
    label = []
    targetlabel = []
    with open(filename, 'r') as f:
        for doc in f.readlines():
            try:
                row = doc.lower().strip().split()
                dict.append(row)
            except:
                pass
    #targetlabel=list(set(np.array(targetlabel)))
    return dict


def _test_LDA(file='cs'):
    n_topics = 10
    n_top_words = 10
    n_samples = 2000
    n_features = 4000

    fileB = [
        '101pitsA_1.txt']#, 'farmer-d.txt', 'kaminski-v.txt', 'kitchen-l.txt', 'lokay-m.txt', 'sanders-r.txt', 'williams-w3.txt']

    filepath = "../../dataset/"

    F_final = {}
    for j, file1 in enumerate(fileB):
        data_samples = readfile1(filepath + str(file1))

        print("Extracting tf features for LDA...")
        tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=n_features,
                                        stop_words='english')
        tf = tf_vectorizer.fit_transform(data_samples)

        print("Fitting LDA models with tf features, n_samples=%d and n_features=%d..."
              % (n_samples, n_features))
        for i in range(1):
            lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=5,
                                        learning_method='online', learning_offset=50.,
                                        random_state=0)
            t0 = time()
            tf_new = lda.fit_transform(tf)
            print(tf_new)

            #print("done in %0.3fs." % (time() - t0))
            tf_feature_names = tf_vectorizer.get_feature_names()
            #print(tf_feature_names)
            get_top_words(lda, tf_feature_names, n_top_words,i)

def get_matrix(sample, vocab):
    final=[]
    for x in sample:
        l=[]
        for i in vocab:
            if (x[i]):
                l.append(x[i])
            else:
                l.append(0)
        final.append(l)
    return final
if __name__ == '__main__':

    # 1st method
    #_test_LDA()

    # 2nd method
    fileB = ['101pitsA_1.txt']

    filepath = "../../dataset/"

    F_final = {}
    for j, file1 in enumerate(fileB):
        data_samples = readfile1(filepath + str(file1))

        #unique vocab size
        vocab=list(set([item for sublist in data_samples for item in sublist]))

        # count vectorier
        sample = make_feature(data_samples)

        # sparse matrix
        x= get_matrix(sample,vocab)
        a=[item for sublist in x for item in sublist]

        # reshaping into sparse matrix. (rows, columns)
        x=np.asarray(a).reshape(len(x),len(vocab))

        #lda
        model = lda.LDA(n_topics=10, n_iter=10, random_state=1)
        model.fit(x)  # model.fit_transform(X) is also available
        topic_word = model.topic_word_  # model.components_ also works
        n_top_words = 10
        for i, topic_dist in enumerate(topic_word):
            topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
            print('Topic {}: {}'.format(i, ' '.join(topic_words)))