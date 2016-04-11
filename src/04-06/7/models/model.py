from __future__ import print_function, division
from utils.lib import *

__author__ = 'george'


class Decision(O):
  def __init__(self, name, low, high):
    self.name = name
    self.low  = low
    self.high = high

  def norm(self, val):
    return norm(val, self.low, self.high)

  def de_norm(self, val):
    return de_norm(val, self.low, self.high)

  def limit(self, val):
    """
    Limit the value between
    low and high
    :param val:
    :return:
    """
    return max(self.low, min(val, self.high))

  def range(self, delta = None):
      if delta is None:
        delta = min((self.high - self.low)/10 , 1)
      n = int((self.high - self.low) / delta)
      return [self.low + i*delta for i in range(n+1)]

class Objective(O):
  def __init__(self, name, low=None, high=None, to_minimize=True):
    self.name = name
    self.low = low
    self.high = high
    self.to_minimize = to_minimize

  def norm(self, val):
    return norm(val, self.low, self.high)

  def de_norm(self, val):
    return de_norm(val, self.low, self.high)

class Constraint(O):
  def __init__(self, name):
    self.name = name
    self.value = None
    self.status = True

class Model(O):
  def __init__(self):
    self.name         = None
    self.decisions    = []
    self.objectives   = []
    self.constraints  = []
    self.population   = []

  def generate(self, generator=uniform):
    count = 0
    while True:
      one = [generator(d.low, d.high) for d in self.decisions]
      status = self.check_constraints(one)
      count+=1
      if status:
        #print("CC : ", count)
        return one

  def evaluate(self, one):
    """
    Evaluate one based on the models
    :param one: Set of decisions to evaluate
    :return: Evaluated set of objectives
    """
    pass

  def evaluate_constraints(self, one):
    """
    Evaluate constraints for set
    of decisions
    :param one: List of decisions
    :return: Status of evaluation and value of offset if constraint fails
    """
    return True, None

  def check_constraints(self, one):
    return True

  def norm_objectives(self, one):
    """
    Normalize objectives
    :param one: Objectives
    :return: Normalized objectives
    """
    return [self.objectives[i].norm(o) for i, o in enumerate(one)]

  def norm_decisions(self, one):
    """
    Normalize decisions
    :param one: Decisions
    :return: Normalized Decisions
    """
    return [self.decisions[i].norm(o) for i, o in enumerate(one)]

  def all_inputs(self, index=0):
    """
    Heavy duty operation. Make sure you know what
    you are doing. Returns all combinations input
    at step 1
    :param index: Index of the decision
    :return:
    """
    def dec_range(lo, hi):
      delta = min((hi-lo)/10 , 1)
      n = int((hi - lo) / delta)
      return [lo + i*delta for i in range(n+1)]

    ds = self.decisions
    ds_range = dec_range(ds[index].low, ds[index].high)
    rets = []
    if index == len(self.decisions)-1:
      for val in ds_range:
        rets.append([val])
      return rets
    else:
      uppers = self.all_inputs(index+1)
      for val in ds_range:
        for upper in uppers:
          rets.append([val]+upper)
    return rets

  def hells(self):
    """
    Get the worst objective for
    :return:
    """
    return [1 if obj.to_minimize else 0 for obj in self.objectives]

  def from_hell(self, obj):
    norms = [self.objectives[i].norm(val) for i, val in enumerate(obj)]
    return [abs(i-j) for i,j in zip(norms, self.hells())]

  def energy(self, obj):
      return 1-(sum(self.from_hell(obj))/len(obj))**0.5
