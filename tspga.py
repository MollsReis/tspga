from data.western_sahara import POINTS, OPTIMAL_SOLUTION
from values import POPULATION, GENERATIONS, SELECTION_PCT, RETAINED_PCT, MUTATION_PCT
from math import hypot
from random import shuffle, randint, sample


# helper function that returns a new shuffled list
def shuffle_ret(lst):
    lst = lst[:]
    shuffle(lst)
    return lst


# object oriented approach to solution
class Solution:
    def __init__(self, points):
        self._distance = None
        self.points = points

    # combine two solutions and return two new ones
    def crossover(self, mate):
        pivot = randint(1, len(self.points) - 1)
        return [Solution([p for p in self.points if p not in mate.points[pivot:]] + mate.points[pivot:]),
                Solution([p for p in self.points if p not in mate.points[:pivot]] + mate.points[:pivot])]

    # randomly swap zero or more pairs of points
    def mutate(self):
        while randint(1, 100) <= (MUTATION_PCT * 100):
            i, j = sample(range(0, len(self.points)), 2)
            self.points[i], self.points[j] = self.points[j], self.points[i]
        return self

    # return total distance of solution (memoized)
    def distance(self):
        if not self._distance:
            self._distance = sum(hypot(pts[0][0] - pts[1][0], pts[0][1] - pts[1][1])
                                 for pts in zip(self.points, (self.points[1:] + self.points[:1])))
        return self._distance


# run the GA algorithm
def solve(points):
    # create initial population
    population = list(Solution(shuffle_ret(points)) for _ in range(POPULATION))

    # generational loop
    for g in range(GENERATIONS):
        population.sort(key=lambda s: s.distance())

        # retain the top solutions for next generation
        retained = population[:][:int(POPULATION * RETAINED_PCT)]

        # grab a larger portion of solutions for crossover
        selection = population[:][:int(POPULATION * SELECTION_PCT)]
        children = []
        while len(selection) > 0:
            # remove a pair of solutions from the selection
            pair = sample(selection, 2)
            selection = [s for s in selection if s not in pair]

            # crossover and mutate the children
            new_children = pair[0].crossover(pair[1])
            children += [c.mutate() for c in new_children]

        # create the new population for the next generation
        population = retained + children

    # return the best solution
    population.sort(key=lambda s: s.distance())
    return population[0].distance()

best = int(solve(POINTS))
print("best after %s gens: %s; optimal: %s; delta: %s (%s%%)" %
      (GENERATIONS,
       best,
       OPTIMAL_SOLUTION,
       best - OPTIMAL_SOLUTION,
       int(((best - OPTIMAL_SOLUTION) / OPTIMAL_SOLUTION) * 100),
       ))
