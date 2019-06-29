
import random


class Offspring:
    def generate_offspring(self, parent_population, domination_counts, crowding_distances, crossover, repair):
        size_population = len(parent_population)
        children = []
        while size_population > len(children):
            potential_parents = [random.randint(0, size_population), random.randint(0, size_population),
                                 random.randint(0, size_population), random.randint(0, size_population)]
            parentA = self.tournament_selection(
                parent_population[potential_parents[0]], parent_population[potential_parents[1]],
                domination_counts[potential_parents[0]], domination_counts[potential_parents[1]],
                crowding_distances[potential_parents[0]], crowding_distances[potential_parents[1]])
            parentB = self.tournament_selection(
                parent_population[potential_parents[2]], parent_population[potential_parents[3]],
                domination_counts[potential_parents[2]], domination_counts[potential_parents[3]],
                crowding_distances[potential_parents[2]], crowding_distances[potential_parents[3]])
            [childA, childB] = crossover.perform_crossover(parentA, parentB)
            childA = repair.get_new_child(childA)
            childB = repair.get_new_child(childB)
            children.append(childA)
            children.append(childB)


    def tournament_selection(self, parentA, parentB, domination_countA, domination_countB, crowding_distA, crowding_distB):
        # see if any parent is less dominated
        if domination_countA < domination_countB:
            winner = parentA
        elif parentB.domination_count < parentA.domination_count:
            winner = parentB
        # else select the most diverse
        elif crowding_distA < crowding_distB:
            winner = parentA
        else:
            winner = parentB
        return winner