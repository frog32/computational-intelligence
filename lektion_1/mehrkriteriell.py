#!/usr/bin/env python
import random
import math


class Fass(object):
    def __init__(self, dna):
        self.dna = dna[:]
        self.age = 0
        self.calculate_data()

    def calculate_data(self):
        width_dna = self.dna[0:5]
        self.d = sum(bit * 2 ** (len(width_dna) - i - 1) for i, bit in enumerate(width_dna))
        height_dna = self.dna[5:10]
        self.h = sum(bit * 2 ** (len(height_dna) - i - 1) for i, bit in enumerate(height_dna))

    def calculate_fitness(self):
        self._fitness = {}
        self._fitness[0] = math.pi * self.d ** 2 / 2 + math.pi * self.d * self.h
        self._fitness[1] = math.pi * self.d ** 2 * self.h / 4

    def mutate(self):
        for i in range(10):
            if random.random() <= 0.01:  # 1% mutation rate
                self.dna[i] = not self.dna[i]
        self.calculate_fitness()
        delattr(self, '_fitness')

    @property
    def fitness(self, i):
        if not hasattr(self, '_fitness'):
            self.calculate_fitness()
        return self._fitness[i]

    def __repr__(self):
        return '<Fass mit d=%s, h=%s, fitness=%s>' % (self.d, self.h, self.fitness)


class Evolutor(object):
    def __init__(self):
        self.my = 30
        self.kappa = 0
        self.delta = 30
        self.ro = 2
        self.rounds = 100
        self.population = []

    def generate_initial_population(self):
        self.population = [Fass([random.randint(0, 1) for j in xrange(10)]) for i in xrange(self.my)]

    def recombinate(self, mariage_pool):
        cut = random.randint(1, 9)
        c = Fass(mariage_pool[0].dna[0:cut] + mariage_pool[1].dna[cut:10])
        d = Fass(mariage_pool[1].dna[0:cut] + mariage_pool[0].dna[cut:10])
        return c, d

    def run(self):
        self.generate_initial_population()

        for round_number in xrange(self.rounds):
            children = []
            # recombination
            while self.delta > len(children):
                mariage_pool = [self.population[random.randint(0, self.my - 1)] for i in range(2)]
                new_children = self.recombinate(mariage_pool)
                children.extend(new_children)

            # mutation
            for child in children:
                child.mutate()

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
