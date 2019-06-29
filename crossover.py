import random


class Crossover:
    def __init__(self, crossover_type):
        self.crossover_type = crossover_type

    def reproduce(self, neighbourhood, population):
        # select two parents from each "neighbourhood"
        # for i_neighbourhood, neighbourhood in enumerate(neighbourhoods):
        iparentB = random.randint(0, len(neighbourhood)-1)
        iparentA = random.randint(0, len(neighbourhood)-1)

        parentA = population[neighbourhood[iparentA]].genotype
        parentB = population[neighbourhood[iparentB]].genotype
        [child, _] = self.perform_crossover(parentA, parentB)
        return child

    def perform_crossover(self, parentA, parentB):
        if self.crossover_type == "Order":
            # Source:
            # https://scholar.google.com/scholar?as_q=Applying+adapting+algorithms+to+epistatic+domains&as_occt=title&hl=en&as_sdt=0%2C31
            num_nodes = len(parentA)
            i = 0  # keep track of which index in the child we are
            crossover_point = random.randint(0, num_nodes-1)  # get a random crossover point
            childA = [None] * num_nodes
            childB = [None] * num_nodes
            childA[0:crossover_point] = parentA[0:crossover_point]
            for city in parentB:
                if city not in childA:
                    childA[crossover_point+i] = city
                    i += 1
            i = 0
            childB[0:crossover_point] = parentB[0:crossover_point]
            for city in parentA:
                if city not in childB:
                    childB[crossover_point + i] = city
                    i += 1
            return [childA, childB]

        elif self.crossover_type == "Cycle":
            pass
        elif self.crossover_type == "PartiallyMatched":
            pass

