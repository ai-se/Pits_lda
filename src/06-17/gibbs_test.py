__author__ = 'amrit'

import numpy as np
import lda
import lda.datasets
import random
random.seed(1)
X = lda.datasets.load_reuters()
vocab = lda.datasets.load_reuters_vocab()
titles = lda.datasets.load_reuters_titles()
print X
model = lda.LDA(n_topics=10, alpha=0.1, eta=0.01,n_iter=100)
model.fit(X)  # model.fit_transform(X) is also available
topic_word = model.topic_word_  # model.components_ also works
n_top_words = 10
for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words + 1):-1]
    print('Topic {}: {}'.format(i, ' '.join(topic_words)))

doc_topic = model.doc_topic_
'''for i in range(10):
    print("{} (top topic: {})".format(titles[i], doc_topic[i].argmax()))'''