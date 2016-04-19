from __future__ import print_function
__author__ = 'george'

from models.schaffer import Schaffer
from models.osyczka import Osyczka2
from models.kursawe import Kursawe
from models.golinski import Golinski
from algorithms.simulated_annealing import SA
from algorithms.max_walk_sat import MWS
from algorithms.de import DE

if __name__ == "__main__":
  for model in [Schaffer, Osyczka2, Kursawe, Golinski]:
    for optimizer in [SA, MWS, DE]:
      print("Optimizer : " + optimizer.__name__)
      o = optimizer(model())
      o.run()
      print("* " * 30)
      print("\n")
