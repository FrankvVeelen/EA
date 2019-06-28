from population import Population
from math import hypot, inf


class Fitness:
    def __init__(self, fitness_type, size_population, num_objectives, weight_vector):
        self.fitness_type = fitness_type
        self.size_population = size_population
        self.num_objectives = num_objectives
        self.weight_vector = weight_vector

        self.fitnesses = [None]*size_population # fitnesses is array of fitness[objective][genotype]
        for i in range(self.size_population):
            self.fitnesses[i] = [None]*self.num_objectives

        self.z_optimum = [inf] * num_objectives  # called z[i] in paper

    def calculate_fitness_pop(self, population, problem):
        if self.fitness_type == "MO_tsp":
            return self.MO_tsp_fitness_pop(population, problem)

    def calculate_fitness_genotype(self, genotype,  problem):
        if self.fitness_type == "MO_tsp":
            return self.MO_tsp_fitness_genotype(genotype, problem)

    def MO_tsp_fitness_pop(self, population, problem):
        for genotype in range(self.size_population):
            for objective in range(self.num_objectives):
                fitness = 0
                # previousCity = population.population[genotype][-1]
                previousCity = None
                for city in population[genotype]:
                    if previousCity is not None:
                        # fitness += hypot(problem.nodes[previousCity].x[objective] - problem.nodes[city].x[objective],
                        #                  problem.nodes[previousCity].y[objective] - problem.nodes[city].y[objective])
                        fitness += distance_between_nodes(problem.nodes[previousCity], problem.nodes[city],
                                                          objective)
                    previousCity = city
                self.fitnesses[genotype][objective] = fitness

    def MO_tsp_fitness_genotype(self, genotype, problem): # TODO use this in the pop function
        fitness_genotype = [0]*self.num_objectives
        for objective in range(self.num_objectives):
            fitness = 0
            # previousCity = population.population[genotype][-1]
            previousCity = None
            for city in genotype:
                if previousCity is not None:
                    fitness += distance_between_nodes(problem.nodes[previousCity], problem.nodes[city], objective)
                previousCity = city
            fitness_genotype[objective] = fitness
        return fitness_genotype

    def calculate_z_optimums_pop(self):
        # find the best genotype for every objective separately
        for objective in range(self.num_objectives):
            for genotype in range(self.size_population):
                if self.fitnesses[genotype][objective] < self.z_optimum[objective]:
                    self.z_optimum[objective] = self.fitnesses[genotype][objective]

    def calculate_z_optimums_genotype(self, genotype_fitness):
        # Check if genotype is better than optimum for each obj separately thus far
        for objective in range(self.num_objectives):
            # print("fitness new child: " + str(genotype_fitness[objective]), "old best: " + str(self.z_optimum))
            if genotype_fitness[objective] < self.z_optimum[objective]:
                self.z_optimum[objective] = genotype_fitness[objective]
                # print("Z optimum was updated")

def distance_between_nodes(nodeA, nodeB, objective):
    distance = hypot(nodeA.x[objective] - nodeB.x[objective], nodeA.y[objective] - nodeB.y[objective])
    return distance
