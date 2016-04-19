from __future__ import print_function, division
__author__ = 'george'
from utils.lib import O

class Point(O):
  id = 0
  def __init__(self, decisions, objectives=None):
    O.__init__(self)
    Point.id += 1
    self.id = Point.id
    self.decisions = decisions
    self.objectives = objectives

  def __hash__(self):
    return hash(self.decisions)

  def __eq__(self, other):
    return cmp(self.decisions, other.decisions) == 0

  def evaluate(self, model):
    if not self.objectives:
      self.objectives = model.evaluate(self.decisions)
    return self.objectives

class Front(O):
  def __init__(self):
    self.points = None
    self.evals = 0

  def update(self, point):
    if self.points is None:
      self.points = []
    self.points.append(point)
    return self

class Algorithm(O):
  """
  Base class Algorithm. All the algorithms
  """
  def __init__(self, model, settings):
    """
    Initialize an algorithm
    :param model:
    :param settings:
    :return:
    """
    O.__init__(self)
    self.model    = model
    self.settings = settings

  def run(self):
    """
    Default runner method for each algorithm.
    :return:
    """
    pass

