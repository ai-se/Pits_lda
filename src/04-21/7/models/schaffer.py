from __future__ import  print_function, division
__author__ = 'george'

from model import *

class Schaffer(Model):
  def __init__(self):
    Model.__init__(self)
    self.name = Schaffer.__name__
    extreme = 10**2
    self.decisions = [Decision("x1", -extreme, extreme)]
    self.objectives = [Objective("f1", low=0, high=extreme**2, to_minimize=True),
                       Objective("f1", low=0, high=(-extreme-2)**2, to_minimize=True)]

  def f1(self, one):
    return one[0]**2

  def f2(self, one):
    return (one[0]-2)**2

  def evaluate(self, one):
    return [self.f1(one), self.f2(one)]

