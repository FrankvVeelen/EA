from domination import a_dominates_b

class Selection:
    def __init__(self, population):
        self.size_population = len(population)
        self.population = population

    def set_dominations(self):
        for individual in self.population:
            individual.domination_count = 0
            individual.set_of_dominations = []
        for p, fitness in enumerate(self.population[:].fitness):
            for q, other_fitness in enumerate(self.population[:].fitness):
                if a_dominates_b(other_fitness, fitness):
                    # this solution is dominated
                    self.population[p].domination_count += 1
                elif a_dominates_b(fitness, other_fitness):
                    # add other solution to the set of dominated solutions
                    self.population[p].set_of_dominations.append(q)

    def sort_dominations(self):
        self.population.sort(key=lambda population: population.domination_count)