from __future__ import print_function, division

__author__ = 'amrit'

import sys
import pickle
from demos import atom
from demos import cmd
import collections
from ldamodel import *
import random

__all__ = ['DE']
Individual = collections.namedtuple('Individual', 'ind fit')


class DE(object):

    def __init__(self, x='rand', y=1, z='bin', F=0.3, CR=0.7):
        self.x = x
        self.y = y
        self.z = z
        self.F = F
        self.CR = CR

    # TODO: add a fitness_aim param?
    # TODO: add a generic way to generate initial pop?
    def solve(self, fitness, initial_population, iterations=10,**r):
        current_generation = [Individual(ind, fitness(*ind,**r)) for ind in
                              initial_population]
        print(current_generation)
        for _ in range(iterations):
            trial_generation = []

            for ind in current_generation:
                v = self._mutate(current_generation)
                u = self._crossover(ind.ind, v)

                trial_generation.append(Individual(u, fitness(*u,**r)))

            current_generation = self._selection(current_generation,
                                                 trial_generation)
        best_index = self._get_best_index(current_generation)
        return current_generation[best_index].ind, current_generation[best_index].fit

    def _mutate(self, population):
        if self.x == 'rand':
            x = tuple(self._get_indices(self.y * 2 + 1, len(population)))

            r1=x[0]
            r=x[1:]

        elif self.x == 'best':
            r1 = self._get_best_index(population)
            r = self._get_indices(self.y * 2, len(population), but='xr1')

        mutated = population[r1].ind[:]  # copy base vector
        dimension = len(mutated)
        difference = [0] * dimension

        for plus in r[:self.y]:
            for i in range(dimension):
                difference[i] += population[plus].ind[i]
        for minus in r[self.y:]:
            for i in range(dimension):
                difference[i] -= population[minus].ind[i]
        for i in range(dimension):
            mutated[i] += self.F * difference[i]
        flag=True
        for i in range(dimension):
            if mutated[i]<bounds[i][0] or mutated[i]>=bounds[i][1]:
                flag=False
        if (flag):
            return mutated
        else:
            return [10,0.5,0.5]


    def _crossover(self, x, v):
        # assume self.z == 'bin'

        u = x[:]
        i = random.randrange(len(x))  # NP

        for j, (a, b) in enumerate(zip(x, v)):
            if i == j or random.random() <= self.CR:
                u[j] = v[j]

        return u

    def _selection(self, current_generation, trial_generation):
        generation = []

        for a, b in zip(current_generation, trial_generation):
            if a.fit > b.fit:
                generation.append(a)
            else:
                generation.append(b)

        return generation

    def _get_indices(self, n, upto, but=None):
        candidates = list(range(upto))

        if but is not None:
            # yeah O(n) but random.sample cannot use a set
            candidates.remove(but)

        return random.sample(candidates, n)

    def _get_best_index(self, population):
        global max_fitness
        best = 0

        for i, x in enumerate(population):
            if x.fit >= max_fitness:
                best = i
                max_fitness=x.fit
        return best

    def _set_x(self, x):
        if x not in ['rand', 'best']:
            raise ValueError("x should be either 'rand' or 'best'.")

        self._x = x

    def _set_y(self, y):
        if y < 1:
            raise ValueError('y should be > 0.')

        self._y = y

    def _set_z(self, z):
        if z != 'bin':
            raise ValueError("z should be 'bin'.")

        self._z = z

    def _set_F(self, F):
        if not 0 <= F <= 2:
            raise ValueError('F should belong to [0, 2].')

        self._F = F

    def _set_CR(self, CR):
        if not 0 <= CR <= 1:
            raise ValueError('CR should belong to [0, 1].')

        self._CR = CR

    x = property(lambda self: self._x, _set_x, doc='How to choose the vector '
                 'to be mutated.')
    y = property(lambda self: self._y, _set_y, doc='The number of difference '
                 'vectors used.')
    z = property(lambda self: self._z, _set_z, doc='Crossover scheme.')
    F = property(lambda self: self._F, _set_F, doc='Weight used during '
                                                   'mutation.')
    CR = property(lambda self: self._CR, _set_CR, doc='Weight used during '
                                                      'bin crossover.')

def cmd(com="demo('-h')"):
  "Convert command line to a function call."
  if len(sys.argv) < 2: return com
  def strp(x): return isinstance(x,basestring)
  def wrap(x): return "'%s'"%x if strp(x) else str(x)
  words = map(wrap,map(atom,sys.argv[2:]))
  return sys.argv[1] + '(' + ','.join(words) + ')'

def _test(file2=''):

    fileB = []
    fileB.append(file2)
    labels=[1,2,3,4, 5 ,6,7,8,9]

    random.seed(1)
    global bounds
    result={}
    for file1 in fileB:
        file_result={}
        for lab in labels:
	    global max_fitness
            max_fitness=0
            print(file1, '\t', lab)
            de = DE(F=0.7, CR=0.3, x='rand')
            pop = [[random.randint(bounds[0][0],bounds[0][1]), random.uniform(bounds[1][0], bounds[1][1]), random.uniform(bounds[2][0],bounds[2][1])]
                   for _ in range(30)]  # 20 * dimension of the problem
            max=0
            for i in [3]:
                v, score = de.solve(main, pop, iterations=i, file=file1,term=lab)
                print(v, '->', score)
                if max < score:
                    max=score
            file_result[lab]=max
        result[file1]=file_result
    print(result)

    with open('dump/'+file2+'.pickle', 'wb') as handle:
        pickle.dump(result, handle)

bounds=[(10,30), (0,1), (0,1)]
max_fitness=0
if __name__ == '__main__':

    eval(cmd())
