import random
import math


class Fass(object):
    def __init__(self, dna):
        self.dna = dna
        width_dna = dna[0:5]
        self.d = sum(bit * 2 ** (len(width_dna) - i - 1) for i, bit in enumerate(width_dna))
        height_dna = dna[5:10]
        self.h = sum(bit * 2 ** (len(height_dna) - i - 1) for i, bit in enumerate(height_dna))

    def calculate_fitness(self):
        self._fitness = math.pi * self.d ** 2 / 2 + math.pi * self.d * self.h
        self._is_valid = math.pi * self.d ** 2 * self.h / 4 >= 300

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

    def __repr__(self):
        return '<Fass mit d=%s, h=%s, fitness=%s>' % (self.d, self.h, self.fitness)


class World(object):
    def __init__(self, parent_count=30, children_count=30, use_mutation=True, use_recombination=False):
        self.use_mutation = use_mutation
        self.use_recombination = use_recombination
        self.parent_count = parent_count
        self.children_count = children_count
        self.population = [Fass([random.randint(0, 1) for j in xrange(10)]) for i in xrange(parent_count)]

    def sort_individuals(self, population):
        population.sort(key=lambda x: x.fitness)

    def eliminate_invalid(self, population):
        return [ind for ind in population if ind.is_valid]

    def recombinate(self, a, b):
        cut = random.randint(1, 9)
        c = Fass(a.dna[0:cut] + b.dna[cut:10])
        d = Fass(b.dna[0:cut] + a.dna[cut:10])
        return c, d

    def mutate(self, ind):
        dna = ind.dna
        for i in range(10):
            if random.random() <= 0.01:
                dna[i] = not dna[i]
        return Fass(dna)

    def generate_next_generation(self):
        # nebenbedingung ausfiltern
        self.sort_individuals(self.population)
        if not len(self.population):
            raise Exception('no individuals left')

        # selection
        sum_ranks = len(self.population) * (len(self.population) + 1) / 2
        # print self.population
        next_generation = []
        for i in range(self.children_count):
            s = 0
            random_number = random.randint(0, sum_ranks)
            for s in range(len(self.population), 0, -1):
                random_number -= s
                if random_number <= 0:
                    next_generation.append(Fass(self.population[s - 1].dna))
                    break
        # next_generation = self.eliminate_invalid(next_generation)
        # recombination
        if self.use_recombination:
            for i in range(10):
                ind1 = random.randint(0, self.children_count - 1)
                ind2 = random.randint(0, self.children_count - 1)
                individual1, individual2 = self.recombinate(next_generation[ind1], next_generation[ind2])
                if len(next_generation) < self.children_count:
                    next_generation.append(individual1)
                else:
                    next_generation[ind1] = individual1
                if len(next_generation) < self.children_count:
                    next_generation.append(individual2)
                else:
                    next_generation[ind2] = individual2

        # mutation
        if self.use_mutation:
            for i in range(len(next_generation)):
                next_generation[i] = self.mutate(next_generation[i])

        next_generation = self.eliminate_invalid(next_generation)
        self.sort_individuals(next_generation)

        self.population = next_generation[0: self.parent_count]


if __name__ == '__main__':
    w = World()
    best = []
    for i in range(1000):
        w.generate_next_generation()
        best.append(w.population[0])
        print 'best value', w.population[0].fitness
