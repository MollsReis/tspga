from data.western_sahara import POINTS, OPTIMAL_SOLUTION
from values import POPULATION, GENERATIONS, RETAINED_PCT, MUTATION_PCT, NEW_PCT
from math import hypot
from random import shuffle, randint, sample, random
import sys


# object oriented approach to solution
class Solution:
    def __init__(self, points):
        self._distance = None
        self.points = points

    # create a random solution from a set of points
    @classmethod
    def random(cls, points):
        points = points[:]
        shuffle(points)
        return cls(points)

    # combine two solutions and return two new ones
    def crossover(self, mate):
        pivot = randint(1, len(self.points) - 1)
        return Solution([p for p in self.points if p not in mate.points[pivot:]] + mate.points[pivot:])

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


# create a weighted list of solutions for a roulette style selection
class Roulette:
    def __init__(self, population):
        distances = [s.distance() for s in population]
        weights = [float(d) / max(distances) for d in distances]
        self.wheel = list(zip(weights, population))

    # grab two samples from the weighted list
    def sample(self):
        samples = ()
        while len(samples) < 2:
            samples += (next(s[1] for s in self.wheel if s[0] > random() and s[1] not in samples),)
        return samples


# GA algorithm
def solve(points):
    # create initial population
    population = [Solution.random(points) for _ in range(POPULATION)]

    # generational loop
    for g in range(GENERATIONS):
        sys.stdout.write("\b\b\b\b\b\b%s%%" % round(g / GENERATIONS * 100, 1))
        sys.stdout.flush()

        # sort the population by distance
        population.sort(key=lambda s: s.distance())

        # retain the top solutions for next generation (elitist selection)
        new_population = population[:int(POPULATION * RETAINED_PCT)]

        # add some random solutions to the population for genetic diversity
        new_population += [Solution.random(points) for _ in range(int(POPULATION * NEW_PCT))]

        # create weighted list of the population (roulette wheel) for crossover selection
        wheel = Roulette(population)

        # crossover and mutate until we get back to our population amount
        while len(new_population) < POPULATION:
            pair = wheel.sample()
            new_population += [pair[0].crossover(pair[1]).mutate()]

        # use the new population for another generation
        population = new_population[:]

    # return the best solution
    population.sort(key=lambda s: s.distance())
    sys.stdout.write("\b\b\b\b\b\b")
    sys.stdout.flush()
    return population[0].distance()

# run the algorithm and output resultsd
best = int(solve(POINTS))
print("best after %s gens: %s; optimal: %s; diff: %s (%s%%)" %
      (GENERATIONS,
       best,
       OPTIMAL_SOLUTION,
       best - OPTIMAL_SOLUTION,
       round(((abs(best - OPTIMAL_SOLUTION)) / ((best + OPTIMAL_SOLUTION) / 2)) * 100, 1),
       ))
