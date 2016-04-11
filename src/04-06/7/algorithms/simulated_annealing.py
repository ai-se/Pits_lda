from __future__ import print_function, division
__author__ = 'george'

from utils.lib import *
from algorithm import *


def default():
  return O(
    kmax      = 1000,  # Max number of iterations
    cooling   = 5,     # Cooling exponent
    gen_size  = 50,    # Size of each generation
    n_prob    = 1,     # probability of neighbor
    verbose   = True   # to display logs
  )

class SA(Algorithm):
  """
  Simulated annealing (SA) is a generic
  probabilistic meta-heuristic for the
  global optimization problem of locating
  a good approximation to the global
  optimum of a given function in a large
  search space
  """
  def __init__(self, model, settings = None):
    if not settings:
      settings = default()
    Algorithm.__init__(self, model, settings)

  @staticmethod
  def anneal(old, new, temp):
    """
    Annealing function
    :param old: Old Energy
    :param new: New Energy
    :param temp: Temperature value
    :return:
    """
    a = exp((old - new)/temp)
    b = rand()
    return  a > b

  def energy(self, decisions, do_norm=True):
    """
    Energy function. Used to evaluate
    :param decisions: Decisions to be evaluated
    :param do_norm: If objectives have to be normalized
    :return: Computed energy value
    """
    norms = []
    objectives = self.model.evaluate(decisions)
    if do_norm:
      for i, obj in enumerate(objectives):
        norms.append(self.model.objectives[i].norm(obj))
      return sum(norms)
    else:
      return sum(objectives)

  def neighbor(self, old):
    """
    Neighbor function to the old value
    :param old:
    :return:
    """
    return self.model.generate() if rand() < self.settings.n_prob else old

  def run(self):
    """
    Runner function to run the simulated annealer
    :return: Best solution and Energy function
    """
    model = self.model
    settings = self.settings
    if settings.verbose:
      print(model)
      print(settings)
    k=0
    evals = 0
    this = model.generate()
    e_this = self.energy(this)
    evals += 1
    best, e_best = this, e_this
    out = ""
    while k < settings.kmax - 1:
      k+=1
      near = self.neighbor(this)
      e_near = self.energy(near)
      evals += 1
      key = " ."
      if e_near < e_this :
        key = " +"
        this, e_this = near, e_near
      elif SA.anneal(e_this, e_near, (1-(k/settings.kmax))**settings.cooling):
        key = " ?"
        this, e_this = near, e_near
      if e_this < e_best:
        key = " !"
        best, e_best = this, e_this
      out += key
      if  k % settings.gen_size == 0 :
        if settings.verbose:
          print(str(round(self.energy(best, do_norm=False), 2)) + out)
        out = ""
    point = Point(best, self.model.evaluate(best))
    front = Front().update(point)
    front.evals = evals
    return front





