from __future__ import print_function, division

__author__ = 'amrit'


import numpy as np
import lda
import lda.datasets
X = lda.datasets.load_reuters()
vocab = lda.datasets.load_reuters_vocab()
titles = lda.datasets.load_reuters_titles()
##rows 395
#print(len(titles))
##columns 4258
#print(len(vocab))
model = lda.LDA(n_topics=20, n_iter=10, random_state=1)
model.fit_transform(X)  # model.fit_transform(X) is also available


#ndz=model.ndz_
#nzw=model.nzw_
#nz=model.nz_
doc_topic = model.doc_topic_
topic_word = model.topic_word_  # model.components_ also works
n_top_words = 8
print(topic_word[0])
for i in range(10):
    print("{} (top topic: {})".format(titles[i], doc_topic[i].argmax()))