from __future__ import print_function, division
__author__ = 'george'
import sys
import numpy as np
from utils.lib import *
from algorithm import *

def default():
  return O(
    gens        = 10,
    max_changes = 100,
    change_prob = 0.5,
    steps       = 10,
    threshold   = 170,
    better      = lt,
    verbose     = True,
    step_size   = 100
  )

class MWS(Algorithm):
  def __init__(self, model, settings=None):
    if not settings:
      settings = default()
    Algorithm.__init__(self, model, settings)

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

  def run(self):
    """
    Runner function to run the
    max walk sat algorithm
    :return: Best solution, Objectives and number of evals
    """
    model = self.model
    settings = self.settings
    if settings.verbose:
      print(model)
      print(settings)

    evals = 0
    decs = model.decisions
    front = Front()
    for _ in range(settings.gens):
      solution = model.generate()
      out = ""
      for __ in range(settings.max_changes):
        evals += 1
        rand_index = choice(range(len(decs)))
        if settings.change_prob < rand():
          clone = list(solution)
          clone[rand_index] = choice(decs[rand_index].range())
          if model.check_constraints(clone):
            solution = clone
            key = " ?"
          else:
            key = " ."
        else:
          cloned, int_evals = self.jiggle_solution(solution, rand_index)
          evals += int_evals
          if cloned != solution:
            key = " +"
            solution = cloned
          else:
            key = " ."
        out+=key
      if settings.verbose:
        print(model.evaluate(solution), out)
      front.update(Point(solution, model.evaluate(solution)))
    front.evals = evals
    return front

  def jiggle_solution(self, solution, index):
    """
    Modify an index in a solution that
    leads to the best solution range in that index
    """
    t_evals = 0
    lo = self.model.decisions[index].low
    hi = self.model.decisions[index].high
    delta = (hi - lo) / self.settings.step_size
    best_soln, best_score = solution, sys.maxint
    if self.settings.better == gt:
      best_score = -best_score
    for val in np.arange(lo, hi+delta, delta):
      cloned = list(solution)
      cloned[index] = val
      t_evals += 1
      if not self.model.check_constraints(cloned):
        continue
      objs = self.model.evaluate(cloned)
      objs = self.model.norm_objectives(objs)
      t_score = sum(objs)
      t_evals += 1
      if self.settings.better(t_score, best_score):
        best_soln, best_score = list(cloned), t_score
    return best_soln, t_evals



