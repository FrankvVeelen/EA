from domination import a_dominates_b
from math import inf

class Selection:
    def __init__(self, population):
        self.size_population = len(population)
        self.o_population = population

    def set_dominations(self, population):
        for individual in population:
            individual.domination_count = 0
            individual.set_of_dominations = []
        for p, individual in enumerate(population):
            for q, other_individual in enumerate(population):
                if a_dominates_b(other_individual.fitness, individual.fitness):
                    # this solution is dominated
                    population[p].domination_count += 1
                elif a_dominates_b(individual.fitness, other_individual.fitness):
                    # add other solution to the set of dominated solutions
                    population[p].set_of_dominations.append(q)

    def sort_dominations(self, population):
        for individual in population:
            print(individual.domination_count)
        population.sort(key=lambda x: x.domination_count)
        for individual in population:
            print(individual.domination_count)

    def find_front(self, i, population):
        front = []
        first_found = False
        for individual in population:
            if individual.domination_count == i:
                front.append(individual)
                first_found = True
            elif first_found:
                break
        return front

    def crowding_distance_assignment(self, I):
        l = len(I)
        I_dist = [0] * l
        for m in range(len(I[0].fitness)):
            I.sort(key=lambda population: population.fitness[m])
            I_dist[0] = I_dist[l - 1] = inf

            for i in range(1, l - 2):
                I_dist[i] = I_dist[i] + (I[i + 1].fitness[m] - I[i - 1].fitness[m]) / (
                            I[i].fitness[-1] - I[i].fitness[0])

    def sort_front(self, front):
        front.sort(key=lambda x: x.crowding_distance, reverse=True)
        return front