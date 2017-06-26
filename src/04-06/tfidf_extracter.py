__author__ = 'amrit'

import numpy as np
from collections import Counter
from demos import cmd

def tf(corpus):
    mat = [token_freqs(doc) for doc in corpus]
    return mat

def token_freqs(doc):
    return Counter(doc[1:])

def tf_idf(mat):
    docs = len(mat)
    word = {}
    doc = {}
    words = 0
    for row in mat:
        for key in row.keys():
            words += row[key]
            try:
                word[key] += row[key]
            except:
                word[key] = row[key]
            try:
                doc[key] += 1
            except:
                doc[key] = 1
    tfidf = {}
    #print(doc)
    for key in doc.keys():
        tfidf[key] = (float(word[key]) / words) * np.log(docs / doc[key])
    return tfidf

def make_feature(corpus, method="tfidf", n_features=1000, file=''):
    mat = tf(corpus)
    f1=open(file,'w')
    if method == "tfidf":
        tfidf = tf_idf(mat)
        ## TOP 5%
        index=int(len(tfidf)*0.05)
        #print(sorted(tfidf.iteritems(), key=lambda (k,v): (v,k), reverse=True))
        keys = np.array(tfidf.keys())[np.argsort(tfidf.values())][-index:]
        #print(keys)
        for row in mat:
            a=zip([key for key in keys], [row[key] for key in keys])
            for k,v in a:
                if v!=0:
                    f1.write((k+' ')*v)
            f1.write('\n')
    f1.close()

def readfile(filename=''):
    corpus = []
    with open(filename, 'r') as f:
        for doc in f.readlines():
            try:
                corpus.append(doc.split())
            except:
                pass

    return corpus

def _test(res=''):
    path = '/share/aagrawa8/Data/Pits/'+str(res)
    path1 = '/share/aagrawa8/Data/process/10'+str(res)
    l=readfile(path)
    make_feature(l, method="tfidf",file=path1)

if __name__ == '__main__':
    eval(cmd())
