from population import Individual
import random


class Offspring:
    def generate_offspring(self, parent_population, crossover, repair, max_exchanges, problem, fitness, mutation):
        size_population = len(parent_population)
        children = []
        while size_population*2-1 > len(parent_population):
            # select 4 random pot. parents
            potential_parents = [random.randint(0, size_population-1), random.randint(0, size_population-1),
                                 random.randint(0, size_population-1), random.randint(0, size_population-1)]
            # perform tournament selection to keep 2
            parentA = self.tournament_selection(parent_population[potential_parents[0]],
                                                parent_population[potential_parents[1]])
            parentB = self.tournament_selection(parent_population[potential_parents[2]],
                                                parent_population[potential_parents[3]])
            # perform crossover
            [childA, childB] = crossover.perform_crossover(parentA.genotype, parentB.genotype)
            # perform mutation
            childA = repair.get_new_child(max_exchanges, problem, childA, fitness.calculate_fitness_genotype(childA, problem), fitness)
            childB = repair.get_new_child(max_exchanges, problem, childB, fitness.calculate_fitness_genotype(childB, problem), fitness)
            # add to children
            o_childA = Individual(childA[0], childA[1])
            o_childA = mutation.mutate(o_childA, fitness, problem)
            o_childB = Individual(childB[0], childB[1])
            o_childB = mutation.mutate(o_childB, fitness, problem)
            parent_population.append(Individual(childA[0], childA[1]))
            parent_population.append(Individual(childB[0], childB[1]))


    def tournament_selection(self, parentA, parentB):
        # see if any parent is less dominated
        if parentA.domination_count < parentB.domination_count:
            winner = parentA
        elif parentB.domination_count < parentA.domination_count:
            winner = parentB
        # else select the most diverse
        elif parentA.crowding_distance > parentB.crowding_distance:
            winner = parentA
        else:
            winner = parentB
        return winner