from __future__ import print_function, division
__author__ = 'amrit'

from ldamodel import *
from scipy.optimize import rosen, differential_evolution

# no_of_topics, doc_topic_prior, topic_word_prior, learning_decay, max_iter
bounds = [ (0,1), (0, 1), (0, 1)]
result = differential_evolution(main, bounds)
print (result)