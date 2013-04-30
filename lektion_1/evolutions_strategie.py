#! /usr/bin/env python

import random
from math import sqrt, pi


class Individual(object):
    def __init__(self, h, d, sigma, tau=None, tau_prime=None):
        self.h = h
        self.d = d
        self.sigma = sigma
        n = 2
        self.tau = tau or (1 / sqrt(2 * sqrt(n)))
        self.tau_prime = tau_prime or (1 / sqrt(2 * n))
        self.age = 0

    def calculate_fitness(self):
        self._fitness = pi * self.d ** 2 / 2 + pi * self.d * self.h
        self._is_valid = pi * self.d ** 2 * self.h / 4 >= 300

    @property
    def fitness(self):
        if not hasattr(self, '_fitness'):
            self.calculate_fitness()
        return self._fitness

    @property
    def is_valid(self):
        if not hasattr(self, '_fitness'):
            self.calculate_fitness()
        return self._is_valid

    def mutate(self):
        self.mutate_strategie()
        self.mutate_object()

    def mutate_strategie(self):
        pass

    def mutate_object(self):
        pass


class Evolutor(object):
    def __init__(self):
        self.my = 7
        self.kappa = 15
        self.delta = 49
        self.ro = 3
        self.rounds = 100
        self.population = []

    def generate_initial_population(self):
        for i in range(self.my):
            h = random.random() * 31
            d = random.random() * 31
            self.population.append(Individual(h=h, d=d, sigma=1))

    def recombinate(self, objects):
        objects_count = len(objects)
        h = sum(map(lambda x: x.h, objects)) / float(objects_count)
        d = sum(map(lambda x: x.d, objects)) / float(objects_count)
        sigma = objects[random.randint(0, objects_count - 1)].sigma
        return Individual(h=h, d=d, sigma=sigma)

    def run(self):
        self.generate_initial_population()

        for round_number in self.rounds:
            children = []
            while self.delta > len(children):
                mariage_pool = [self.population[random.randint(0, self.my - 1)] for i in range(3)]
                child = self.recombinate(mariage_pool)
                child.mutate()
                if child.is_valid:
                    children.append(child)

            # selection
            # eliminate all overaged individuals
            self.population = [ind for ind in self.population if ind.age <= self.kappa]

            # sort with fitness and trow away all individuals which couldn't make it into the next round
            self.population = sorted(self.population + children)[0:self.my]

            # make every individual older
            for ind in self.population:
                ind.age += 1

if __name__ == '__main__':
    e = Evolutor()
    e.run()
