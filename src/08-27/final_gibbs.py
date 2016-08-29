from __future__ import print_function, division

__author__ = 'amrit'

from random import randint, random, seed, shuffle, sample
import lda
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn import svm
from sklearn.feature_extraction import FeatureHasher
from time import time
import pickle
import sys

from ABCD import ABCD


def main(**r):
    # 1st r
    start_time = time()
    data_samples = r['data_samples']
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
    tf = tf_vectorizer.fit_transform(data_samples)

    lda1 = lda.LDA(n_topics=int(r['k']), alpha=r['alpha'], eta=r['beta'], n_iter=100)

    lda1.fit_transform(tf)
    docs = []
    tops = lda1.doc_topic_
    print(tops[0])
    print(tops[0].argmax())
    divider = randint(0, int(r['k']) - 1)

    '''for i in range(len(data_samples)):
        if tops[i].argmax() == divider:
            docs.append(data_samples[i] + ' >>> yes')
        else:
            docs.append(data_samples[i] + ' >>> no')'''

    _test(tops, file=r['file'].split('.')[0].strip(), targetlist=r['target'])


"vocabulary"


def vocabulary(lst_of_words):
    v = []
    for c in lst_of_words:
        v.extend(c[1:])
    return list(set(v))


"term frequency "


def token_freqs(doc):
    return Counter(doc[1:])


"tf"


def tf(corpus):
    mat = [token_freqs(doc) for doc in corpus]
    return mat


def l2normalize(mat):
    for row in mat:
        n = 0
        for key in row:
            n += row[key] ** 2
        n = n ** 0.5
        for key in row:
            row[key] = row[key] / n
    return mat


"hashing trick"


def hash(mat, n_features=1000):
    hasher = FeatureHasher(n_features=n_features)
    X = hasher.transform(mat)
    X = X.toarray()
    return X


"make feature matrix"


def make_feature(corpus, method="tfidf", n_features=1000):
    label = list(zip(*corpus)[0])
    mat = tf(corpus)
    matt = hash(mat, n_features=n_features)
    return matt, label


"split data according to target label"


def split_two(corpus, label, target_label):
    pos = []
    neg = []
    for i, lab in enumerate(label):
        if lab == target_label:
            pos.append(i)
        else:
            neg.append(i)
    print(pos)
    ## corpus is of dictionary type.
    positive = corpus[pos]
    negative = corpus[neg]
    print(positive)
    return {'pos': positive, 'neg': negative}


"smote"


def smote(data, num, k=5):
    corpus = []
    nbrs = NearestNeighbors(n_neighbors=k + 1, algorithm='ball_tree').fit(data)
    distances, indices = nbrs.kneighbors(data)
    for i in range(0, num):
        mid = randint(0, len(data) - 1)
        nn = indices[mid, randint(1, k)]
        datamade = []
        for j in range(0, len(data[mid])):
            gap = random()
            datamade.append((data[nn, j] - data[mid, j]) * gap + data[mid, j])
        corpus.append(datamade)
    corpus = np.array(corpus)
    return corpus


"SVM"


def do_SVM(train_data, test_data, train_label, test_label):
    clf = svm.LinearSVC(dual=False)
    clf.fit(train_data, train_label)
    prediction = clf.predict(test_data)
    abcd = ABCD(before=test_label, after=prediction)
    F = np.array([k.stats()[-2] for k in abcd()])
    labeltwo = list(set(test_label))
    if labeltwo[0] == 'positive':
        labelone = 0
    else:
        labelone = 1
    try:
        return F[labelone]
    except:
        pass


"cross validation"


def cross_val(data=[], thres=[0.02, 0.05], folds=5,
              feature="tfidf", is_shingle="no_shingle", n_feature=1000, target=[]):
    "split for cross validation"

    def cross_split(corpus, folds, index):
        i_major = []
        i_minor = []
        l = len(corpus)
        for i in range(0, folds):
            if i == index:
                i_minor.extend(range(int(i * l / folds), int((i + 1) * l / folds)))
            else:
                i_major.extend(range(int(i * l / folds), int((i + 1) * l / folds)))
        return corpus[i_minor], corpus[i_major]

    "generate training set and testing set"

    def train_test(pos, neg, folds, index, issmote="no_smote", neighbors=5):
        pos_train, pos_test = cross_split(pos, folds=folds, index=index)
        neg_train, neg_test = cross_split(neg, folds=folds, index=index)
        if issmote == "smote":
            num = int((len(pos_train) + len(neg_train)) / 2)
            pos_train = smote(pos_train, num, k=neighbors)
            neg_train = neg_train[np.random.choice(len(neg_train), num, replace=False)]
        data_train = np.vstack((pos_train, neg_train))
        data_test = np.vstack((pos_test, neg_test))
        label_train = ['pos'] * len(pos_train) + ['neg'] * len(neg_train)
        label_test = ['pos'] * len(pos_test) + ['neg'] * len(neg_test)

        "Shuffle"
        tmp = range(0, len(label_train))
        shuffle(tmp)
        data_train = data_train[tmp]
        label_train = np.array(label_train)[tmp]

        tmp = range(0, len(label_test))
        shuffle(tmp)
        data_test = data_test[tmp]
        label_test = np.array(label_test)[tmp]

        return data_train, data_test, label_train, label_test

    #load = readfile(data=data, is_shingle=is_shingle, thres=thres)
    # = load['corpus']
    #targetlist = load['targetlist']
    target_label = 'yes'

    #data, label = make_feature(corpus, method=feature, n_features=n_feature)
    #print(data, label)
    split = split_two(corpus=data, label=target, target_label=target_label)
    pos = split['pos']
    neg = split['neg']

    # sys.stdout.write(filename + ": " + str(len(pos)) + " " + target_label + " in " + str(len(label))+'\n')

    result = []
    for i in range(folds):
        tmp = range(0, len(pos))
        shuffle(tmp)
        pos = pos[tmp]
        tmp = range(0, len(neg))
        shuffle(tmp)
        neg = neg[tmp]
        for index in range(folds):
            data_train, data_test, label_train, label_test = \
                train_test(pos, neg, folds=folds, index=index, issmote="no_smote", neighbors=5)
            "SVM"
            result.append(do_SVM(data_train, data_test, label_train, label_test))
    return result


def readfile(data=[], is_shingle="no_shingle", thres=[0.02, 0.05]):
    corpus = []
    targetlist = []
    labellst = []
    for doc in data:
        try:
            label = doc.lower().split(' >>> ')[1].split()[0]
            labellst.append(label)
            corpus.append([label] + doc.split(' >>> ')[0].split())
        except:
            pass
    ##no of rows
    l = len(corpus)
    labelcount = Counter(labellst)
    labellst = list(set(labellst))
    '''while True:
        for label in labellst:
            if labelcount[label] > l * thres[0] and labelcount[label] < l * thres[1]:
                targetlist.append(label)
        if targetlist: break
        thres[1] = 2 * thres[1]
        thres[0] = 0.5 * thres[0]'''

    #return {'corpus': corpus, 'targetlist': targetlist}
    return {'corpus': corpus, 'targetlist': labellst}


def _test(data=[],file='', targetlist=[]):
    thres = [0.02, 0.05]

    issel = ["tf"]
    isshingle = ["no_shingle"]
    # issmote = ["no_smote"]
    F_final = {}
    # temp_file = {}
    temp_file = {}
    F_final[file] = temp_file = cross_val(data=data, thres=thres,
                                                 folds=5,
                                                 n_feature=10000, target=targetlist)
    print(F_final)
    print("\n")
    tmp = []

    with open('dump/' + file + '_SE_DE.pickle', 'wb') as handle:
        pickle.dump(F_final, handle)