import random


class Mutation:
    def __init__(self, mutation_type, mutation_chance):
        self.mutation_type = mutation_type
        self.mutation_chance = mutation_chance

    def mutate(self, individual, fitness, problem):
        if random.random() < self.mutation_chance:
            gen_length = len(individual.genotype)
            if self.mutation_type == "RSM":
                start = random.randint(0, gen_length-1)
                stop = random.randint(start, gen_length)
                individual.genotype[start:stop] = reversed(individual.genotype[start:stop])
                individual.fitness = fitness.calculate_fitness_genotype(individual.genotype, problem)
        return individual
