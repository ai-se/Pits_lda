from __future__ import print_function, division
__author__ = 'panzer'
from model import *
from math import sqrt, sin

class Kursawe(Model):
  def __init__(self):
    Model.__init__(self)
    self.name = Kursawe.__name__
    self.decisions=[]
    self.decisions.append(Decision("x1", -5, 5))
    self.decisions.append(Decision("x2", -5, 5))
    self.decisions.append(Decision("x3", -5, 5))
    self.objectives = []
    self.objectives.append(Objective("f1", -20, -4.86, to_minimize=True))
    self.objectives.append(Objective("f2", -9.63, 22.90, to_minimize=True))

  def evaluate(self, one):
    return [Kursawe.f1(one), Kursawe.f2(one)]

  @staticmethod
  def f1(ds):
    total = 0
    for i in range(len(ds)-1):
      e = -0.2 * sqrt(ds[i]**2 + ds[i+1]**2)
      total+= -10*exp(e)
    return total

  @staticmethod
  def f2(ds):
    total = 0
    for i in range(len(ds)):
      total+= abs(ds[i])**0.8 + 5*sin(ds[i]**3)
    return total

  @staticmethod
  def get_extreme_objectives():
    o = Kursawe()
    f1s = []
    f2s = []
    for one in o.all_inputs():
      f1s.append(Kursawe.f1(one))
      f2s.append(Kursawe.f2(one))
    print(min(f1s), max(f1s))
    print(min(f2s), max(f2s))
