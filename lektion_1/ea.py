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
    def __init__(self, count=30):
        self.count = count
        self.population = [Fass([random.randint(0, 1) for j in xrange(10)]) for i in xrange(count)]

    @property
    def ranking(self):
        return list(enumerate(sorted(self.population, key=lambda x: x.fitness, reverse=True)))

    def recombinate(self, a, b):
        cut = random.randint(1, 9)
        c = Fass(a.dna[0:cut] + b.dna[cut:10])
        d = Fass(b.dna[0:cut] + a.dna[cut:10])
        return c, d

    def mutate(self, ind):
        dna = ind.dna
        for i in range(10):
            if random.randint(1, 10) == 1:
                dna[i] = not dna[i]
        return Fass(dna)

    def generate_next_generation(self):
        ranking = self.ranking
        print 'ranking', ranking
        sum_ranks = sum(map(lambda x: x[0], ranking))
        print 'sum_ranks', sum_ranks

        selection = []
        for i in range(self.count):
            s = 0
            random_number = random.randint(0, sum_ranks)
            for rank, ind in ranking:
                if random_number <= s + rank:
                    selection.append(ind)
                    break
                s += rank

        next_round = []
        for i in range(self.count / 2):
            c, d = self.recombinate(selection[random.randint(0, self.count - 1)], selection[random.randint(0, self.count - 1)])
            c = self.mutate(c)
            d = self.mutate(d)
            next_round.append(c)
            next_round.append(c)
        self.population = next_round
