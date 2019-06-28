import random


class Population:
    def __init__(self, n, num_nodes):
        # creates initial population
        self.population_size = n
        self.population = [0] * n
        self.elite_population = []
        self.elite_fitnesses = []
        for i in range(0, n):
            self.population[i] = generate_genotype("OrderBased", 0, num_nodes)
        #print("Initial population: ")
        #print(self.population)

    def add_to_elite(self, genotype, genotype_fitnesses):
        if self.is_dominated_by_EP(genotype_fitnesses) == False:
            self.elite_population.append(genotype)
            self.elite_fitnesses.append(genotype_fitnesses)

    def is_dominated_by_EP(self, genotype_fitness):
        flag = False
        for elite, elite_fitness in zip(self.elite_population, self.elite_fitnesses):
            #print(str(elite) + str(elite_fitness))
            domination_count = 0
            for i in range(len(elite_fitness)):
                if genotype_fitness[i] >= elite_fitness[i]:
                    domination_count += 1
            #print("Count: " + str(domination_count) + "Thres: " + str(len(elite_fitness)))
            if domination_count == len(elite_fitness):
                flag = True
                #print("not adding to EP")
        return flag

    def remove_dominated_EP_by_child(self, genotype_fitness):
        for elite, elite_fitness in zip(self.elite_population, self.elite_fitnesses):
            if self.find_dominated_EP_by_child(genotype_fitness, elite_fitness):
                self.elite_population.remove(elite)
                self.elite_fitnesses.remove(elite_fitness)

    def find_dominated_EP_by_child(self, genotype_fitness, elite_fitness):
        flag = False
        if all(elite_fitness[i] > fitness for i, fitness in enumerate(genotype_fitness)):
            flag = True
            print("removing from EP")
        return flag

    # def check_for_dominated_solutions(self, fitnesses, num_objectives):
    #     for elite, elite_fitness in zip(self.elite_population, self.elite_fitnesses):
    #         if self.check_domination(fitnesses, elite_fitness, num_objectives):
    #             self.elite_population.remove(elite)
    #
    # def check_domination(self, fitnesses, elite_fitness, num_objectives):
    #     # return 1 if elite solution is dominated, 0  if non-dominated
    #     for genotype in range(self.population_size):
    #         domination_count = 0
    #         for objective in range(num_objectives):
    #             if fitnesses[objective][genotype] <= elite_fitness[objective]:  # also remove exact copies
    #                 domination_count += 1
    #         if domination_count == num_objectives:  # dominated for all objectives, no longer elite
    #             print("An elite solution will be removed")
    #             return 1
    #     # if code has reached this solution is not dominated
    #     return 0


# https://ieeexplore.ieee.org/document/1134123
def generate_genotype(encoding, length, num_nodes):
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