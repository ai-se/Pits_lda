from __future__ import print_function, division
from collections import Counter
#from pdb import set_trace
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn import svm
from sklearn.feature_extraction import FeatureHasher
from random import randint, random, seed, shuffle
from time import time
from collections import defaultdict
from sk import rdivDemo
from copy import deepcopy
import matplotlib.pyplot as plt
import pickle
from demos import atom
from demos import cmd
import sys

from ABCD import ABCD

"Decorator to report arguments and time taken"


def run(func):
    def inner(*args, **kwargs):
        t0 = time()
        print("You are running: %s" % func.__name__)
        print("Arguments were: %s, %s" % (args, kwargs))
        result = func(*args, **kwargs)
        print("Time taken: %f secs" % (time() - t0))
        return result

    return inner


def timer(func):
    def inner(*args, **kwargs):
        t0 = time()
        result = func(*args, **kwargs)
        print("%s takes time: %s secs" % (func.__name__, time() - t0))
        return result

    return inner


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


"tf-idf"


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
    for key in doc.keys():
        tfidf[key] = word[key] / words * np.log(docs / doc[key])
    return tfidf


"L2 normalization"


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


tfidf_temp = {}
filename_global = ""
lastfile = ""

"make feature matrix"


def make_feature(corpus, method="tfidf", n_features=1000):
    label = list(zip(*corpus)[0])
    mat = tf(corpus)
    if method == "tfidf":
        tfidf = tf_idf(mat)
        keys = np.array(tfidf.keys())[np.argsort(tfidf.values())][-n_features:]
        matt = []
        for row in mat:
            matt.append([row[key] for key in keys])
        matt = np.array(matt)
        # matt=norm(matt)


        "Store tfidf_temp for drawing"
        global tfidf_temp
        if filename_global not in tfidf_temp.keys():
            tfidf_temp[filename_global] = np.sort(tfidf.values())


    else:
        matt = hash(mat, n_features=n_features)
       # matt = norm(matt)
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
    positive = corpus[pos]
    negative = corpus[neg]
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


def cross_val(filename='', filepath='', filetype='.txt', thres=[0.02, 0.05], folds=10,
               feature="tfidf", is_shingle="no_shingle", n_feature=1000):
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

    load = readfile(filename=filepath + filename + filetype, is_shingle=is_shingle, thres=thres)
    corpus = load['corpus']
    targetlist = load['targetlist']
    target_label = targetlist[0]

    data, label = make_feature(corpus, method=feature, n_features=n_feature)
    split = split_two(corpus=data, label=label, target_label=target_label)
    pos = split['pos']
    neg = split['neg']

    #sys.stdout.write(filename + ": " + str(len(pos)) + " " + target_label + " in " + str(len(label))+'\n')

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


"Load data from file to list of lists"


def readfile(filename='', is_shingle="no_shingle", thres=[0.02, 0.05]):
    corpus = []
    targetlist = []
    labellst = []
    with open(filename, 'r') as f:
        for doc in f.readlines():
            try:
                label = doc.lower().split(' >>> ')[1].split()[0]
                labellst.append(label)
                if is_shingle=="no_shingle":
                   corpus.append([label] + doc.split(' >>> ')[0].split())
                elif is_shingle=="bigram":
                   corpus.append([label] + shingle(doc.split(' >>> ')[0], n=2))
                elif is_shingle=="trigram":
                   corpus.append([label] + shingle(doc.split(' >>> ')[0], n=3))

            except:
                pass
        l = len(corpus)
        labelcount = Counter(labellst)
        labellst = list(set(labellst))
        while True:
            for label in labellst:
                if labelcount[label] > l * thres[0] and labelcount[label] < l * thres[1]:
                    targetlist.append(label)
            if targetlist: break
            thres[1] = 2 * thres[1]
            thres[0] = 0.5 * thres[0]
    return {'corpus': corpus, 'targetlist': targetlist}


def shingle(str, n=3):
    x = str.split()
    a = []
    for token in x:
        a.append(list(token))

    b = []
    for tokens in a:
        x = [tokens[i:i + n] for i in range(len(tokens) - n + 1) if len(tokens[i]) < 4]
        for l in x:
            b.append(''.join(l))
    return (list(set(b)))
    
def cmd(com="demo('-h')"):
  "Convert command line to a function call."
  if len(sys.argv) < 2: return com
  def strp(x): return isinstance(x,basestring)
  def wrap(x): return "'%s'"%x if strp(x) else str(x)  
  words = map(wrap,map(atom,sys.argv[2:]))
  return sys.argv[1] + '(' + ','.join(words) + ')'

class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

def _test(file='cs'):
    filepath = '/share/aagrawa8/Data/SE/'
    thres = [0.02, 0.05]
    issel = ["tf"]
    isshingle=["no_shingle"]
        #issmote = ["no_smote"]
    F_final = {}
        #temp_file = {}
    temp_file={}
    for feature in issel:
        temp_feature={}
        for is_shingle in isshingle:
            temp_feature[is_shingle] = cross_val(filename=file, filepath=filepath, filetype='.txt', thres=thres,
                                                    folds=5, feature=feature, is_shingle=is_shingle,
                                                   n_feature=10000)
            #temp_file=temp_feature
        temp_file[feature]=temp_feature
    F_final[file] = temp_file
    #"Scott-knot"
    #print(filename + ":")
    print(F_final)
    print ("\n")

    with open('dump/'+file+'_baseline.pickle', 'wb') as handle:
        pickle.dump(F_final, handle)

if __name__ == '__main__':
    
    eval(cmd())
