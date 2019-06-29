import random
from domination import a_dominates_b
from math import inf
class Population:
    def __init__(self, n, num_nodes, num_objectives):
        # creates initial population
        self.population_size = n
        self.population = [0] * n
        self.elite_population = []
        self.elite_fitnesses = []
        for i in range(0, n):
            self.population[i] = Individual(generate_genotype("OrderBased", num_nodes), [inf]*num_objectives)

    def add_to_elite(self, genotype, genotype_fitnesses):
        self.remove_dominated_EP_by_child(genotype_fitnesses) # first remove the elite that will be dominated by this solution
        if self.is_dominated_by_EP(genotype_fitnesses) == False: # then see if this solution has to be added
            self.elite_population.append(genotype)
            self.elite_fitnesses.append(genotype_fitnesses)

    def is_dominated_by_EP(self, genotype_fitness):
        # flag = False
        for elite, elite_fitness in zip(self.elite_population, self.elite_fitnesses):
            if a_dominates_b(elite_fitness, genotype_fitness):
                return True
        return False

    def remove_dominated_EP_by_child(self, genotype_fitness):
        for elite, elite_fitness in zip(self.elite_population, self.elite_fitnesses):
            if a_dominates_b(genotype_fitness, elite_fitness):
                self.elite_population.remove(elite)
                self.elite_fitnesses.remove(elite_fitness)

class Individual:
    def __init__(self, genotype, fitness, domination_count = inf, crowding_distance = 0):
        self.genotype = genotype
        self.fitness = fitness
        self.domination_count = domination_count
        self.crowding_distance = crowding_distance


# https://ieeexplore.ieee.org/document/1134123
def generate_genotype(encoding, num_nodes):
    genotype = list(range(0, num_nodes))
    if encoding == "OrderBased":
        random.shuffle(genotype)  # generate random order of cities
        return genotype
    elif encoding == "Analytic":
        return 0
    elif encoding == "LocusBased":
        return 0
    elif encoding == "MultiDimensional":
        return 0