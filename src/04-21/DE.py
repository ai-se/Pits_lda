from __future__ import print_function, division
__author__ = 'amrit'

from ldamodel import *
from scipy.optimize import rosen, differential_evolution
import random

# no_of_topics, doc_topic_prior (a), topic_word_prior (b), learning_decay, max_iter
random.seed(1)
bounds = [(10,30), (0,1), (0, 1), (0, 1)]
result = differential_evolution(main, bounds, maxiter=10, popsize=10)
print (result)