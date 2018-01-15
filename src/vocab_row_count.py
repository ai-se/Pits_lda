from __future__ import print_function, division

__author__ = 'amrit'

import sys

sys.dont_write_bytecode = True
import pandas as pd
from Preprocess import *
from sklearn.feature_extraction.text import CountVectorizer
#citemap=rows=15121, size=7506
#pitsA=965,size=154
#pitsB=1650,size=137
#pitsC=323,size=42
#pitsD=182,size=50
#pitsE=825,size=140
#pitsF=744,size=100
#SO=895621, size=98548


# df=pd.read_csv("../dataset/citemap.csv",sep="\$\|\$", engine='python')
# df['text']=df[['Title', 'Abstract']].apply(lambda x: x[0] if x[1]=="None" else x[0] + ' ' + x[1], axis=1)
# df['text']=df['text'].apply(lambda x: process(x, string_lower, punctuate_preproc,
#                        numeric_isolation, stopwords, stemming, word_len_less))
# df['text'].to_csv("../dataset/preproc_citemap.csv",index=False,header=['Text'])

# df=pd.read_csv("../dataset/preproc_citemap.csv")
# tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
# samples=df['Text'].values
# tf = tf_vectorizer.fit_transform(samples)
# print(len(tf_vectorizer.get_feature_names()))

l=[]
with open("../dataset/SO",mode='r') as f:
    for lin in f.readlines():
        l.append(lin.strip())
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
tf = tf_vectorizer.fit_transform(l)
print(len(l),len(tf_vectorizer.get_feature_names()))