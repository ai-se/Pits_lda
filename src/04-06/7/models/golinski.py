from __future__ import print_function, division
__author__ = 'george'

from model import *

class Golinski(Model):
  def __init__(self):
    Model.__init__(self)
    self.name = Golinski.__name__
    self.decisions = []
    self.decisions.append(Decision("x1", 2.6, 3.6))
    self.decisions.append(Decision("x2", 0.7, 0.8))
    self.decisions.append(Decision("x3", 17.0, 28.0))
    self.decisions.append(Decision("x4", 7.3, 8.3))
    self.decisions.append(Decision("x5", 7.3, 8.3))
    self.decisions.append(Decision("x6", 2.9, 3.9))
    self.decisions.append(Decision("x7", 5.0, 5.5))
    self.objectives = []
    self.objectives.append(Objective("f1", 2352.34, 7144.70, to_minimize=True))
    self.objectives.append(Objective("f2", 694.23, 1699.0, to_minimize=True))
    self.constraints = ["g1","g2","g3","g4","g5","g6",
                        "g7","g8","g9","g10","g11"]

  def check_constraints(self, d):
    verbose = False
    """
    Check if the constraints are satisfied for a set of decisions
    :param d:  Decisions d to check constraints for.
    :return: status of constraints
    """
    # g1(x)
    status = 1/(d[0]* d[1]**2 * d[2]) - 1/27 <= 0
    # g2(x)
    status = status and (1/(d[0]* d[1]**2 * d[2]**2) - 1/397.5 <= 0)
    # g3(x)
    status = status and (d[3]**3/(d[1] * d[2]**2 * d[5]**4) - 1/1.93 <= 0)
    # g4(x)
    status = status and (d[4]**3/(d[1] * d[2] * d[6]**4) - 1/1.93 <= 0)
    # g5(x)
    status = status and (d[1]*d[2] - 40 <= 0)
    # g6(x)
    status = status and (d[0]/d[1] - 12 <= 0)
    # g7(x)
    status = status and (5 - d[0]/d[1] <= 0)
    # g8(x)
    status = status and (1.9 - d[3] +1.5*d[5] <= 0)
    # g9(x)
    status = status and (1.9 - d[4] +1.1*d[6] <= 0)
    # g10(x)
    status = status and (Golinski.f2(d) <= 1300)
    # g11(x)
    a = 745*d[4]/(d[1]*d[2])
    b = 1.575 * 10**8
    status = status and ((a**2 + b)**0.5 / (0.1 * d[6]**3) <= 1100)
    return status

  def evaluate(self, one):
    return [Golinski.f1(one), Golinski.f2(one)]

  @staticmethod
  def f1(d):
    return 0.7854 * d[0] * (d[1]**2) * (10*(d[2]**2)/3 + 14.933*d[2] - 43.0934) - \
           1.508 * d[0] * (d[5]**2 + d[6]**2) + \
           7.477 * (d[5]**3 + d[6]**3) + \
           0.7854 * (d[3]*(d[5]**2) + d[4]*(d[6]**2))

  @staticmethod
  def f2(d):
    num = (745 * d[3] / (d[1]*d[2]))**2 + 1.69*10**7
    den = 0.1 * d[5]**3
    return num**0.5 / den

  @staticmethod
  def get_extreme_objectives():
    o = Golinski()
    f1s = []
    f2s = []
    for one in o.all_inputs():
      f1s.append(Golinski.f1(one))
      f2s.append(Golinski.f2(one))
    print(min(f1s), max(f1s))
    print(min(f2s), max(f2s))
