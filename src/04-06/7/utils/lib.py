from __future__ import print_function, division
import sys, random, math
__author__ = 'george'

"""
CONSTANTS
"""
EPS = 0.000001

class O():
  """
  Default class which everything extends.
  """
  def __init__(self, **d):
    self.has().update(**d)

  def has(self):
    return self.__dict__

  def update(self, **d):
    self.has().update(d)
    return self

  def __repr__(self):
    show = [':%s %s' % (k,self.has()[k])
      for k in sorted(self.has().keys())
      if k[0] is not "_"]
    txt = ' '.join(show)
    if len(txt) > 60:
      show=map(lambda x: '\t'+x+'\n',show)
    return '{'+' '.join(show)+'}'

  def __getitem__(self, item):
    return self.has().get(item)

  def __setitem__(self, key, value):
    self.has()[key] = value


def norm(x, low, high):
  """
  Method to normalize value
  between 0 and 1
  """
  nor = (x - low)/(high - low + EPS)
  if nor > 1:
    return 1
  elif nor < 0:
    return 0
  return nor


def de_norm(x, low, high):
  """
  Method to de-normalize value
  between low and high
  """
  de_nor = x*(high-low) + low
  if de_nor > high:
    return high
  elif de_nor < low:
    return low
  return de_nor

def say(*lst):
  print(*lst, end="")
  sys.stdout.flush()

def uniform(low, high):
  """
  Uniform value between low and high
  :param low: Lower value for uniform distribution
  :param high: Upper value for uniform distribution
  :return: Return random value from a uniform distribution between low and high
  """
  return random.uniform(low, high)

def choice(lst):
  """
  Random value from lst
  :param lst: List to select a random element
  :return: Return a random value
  """
  return random.choice(lst)

def rand():
  return random.random()

def exp(val):
  return math.e**val

def avg(lst):
  return sum(lst)/len(lst)

def lt(a, b):
  return a < b

def gt(a, b):
  return a > b

def lte(a, b):
  return a <= b

def gte(a, b):
  return a >= b

def within(start, stop, step=1):
  """
  Generate a random number between a range
  :param start: start value
  :param stop: stop value
  :param step: increment value
  :return:
  """
  mul = int(1/step)
  return random.randrange(start*mul, stop*mul, 1) * step

def seed(val = None):
  random.seed(val)

def trunc(x, n=3):
  if isinstance(x, list):
    return [round(i, n) for i in x]
  else:
    return round(x, n)