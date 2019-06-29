
import random


class Offspring:
    def generate_offspring(self, parent_population, crossover, repair):
        size_population = len(parent_population)
        children = []
        while size_population*2 > len(parent_population):
            # select 4 random pot. parents
            potential_parents = [random.randint(0, size_population), random.randint(0, size_population),
                                 random.randint(0, size_population), random.randint(0, size_population)]
            # perform tournament selection to keep 2
            parentA = self.tournament_selection(parent_population[potential_parents[0]],
                                                parent_population[potential_parents[1]])
            parentB = self.tournament_selection(parent_population[potential_parents[2]],
                                                parent_population[potential_parents[3]])
            # perform crossover
            [childA, childB] = crossover.perform_crossover(parentA, parentB)
            # perform mutation
            childA = repair.get_new_child(childA)
            childB = repair.get_new_child(childB)
            # add to children
            parent_population.append(childA)
            parent_population.append(childB)


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