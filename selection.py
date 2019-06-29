from domination import a_dominates_b

class Selection:
    def __init__(self, size_population):
        self.size_population = size_population
        self.domination_count = [0] * size_population
        self.set_of_dominations = [0] * self.size_population
        self.front1 = []

    def set_dominations(self, population_fitnesses):
        self.domination_count = [0] * self.size_population
        self.set_of_dominations = [0] * self.size_population
        for p, fitness in enumerate(population_fitnesses):
            for q, other_fitness in enumerate(population_fitnesses):
                if a_dominates_b(other_fitness, fitness):
                    # this solution is dominated
                    self.domination_count[p] += 1
                elif a_dominates_b(fitness, other_fitness):
                    # add other solution to the set of dominated solutions
                    if self.set_of_dominations[p] == 0:
                        self.set_of_dominations[p] = [q]
                    else:
                        self.set_of_dominations[p].append(q)
            self.domination_count[p] -= 1  # remove the domination count for the solution self
        for i, count in enumerate(self.domination_count):
            if self.domination_count[i] == 0:
                # this is a first front solution
                self.front1.append(i)


    def sort_dominations(self):
        sorted_fronts = [x for _, x in sorted(zip(self.domination_count, list(range(len(self.domination_count)))))]
        print(sorted_fronts)