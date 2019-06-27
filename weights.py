from math import sqrt, inf


class Weights:
    def __init__(self, num_obj, num_neighbors):
        self.num_objectives = num_obj
        self.num_neighbors = num_neighbors
        self.weights = [0] * num_obj
        self.generate_objective_weights()
        self.neighbourhoods = [0] * num_obj #neighbours for weight[i] are itself and the closest weight vectors
        for i in range(num_obj):
            self.neighbourhoods[i] = [0] * num_neighbors
        self.find_neighbors()

    def generate_objective_weights(self):
        if self.num_objectives == 2:
            self.weights[0] = [0.3, 1]
            self.weights[1] = [1, 0.3]
        elif self.num_objectives == 3:
            self.weights[0] = [0.5, 0.75, 1]
            self.weights[1] = [1, 0.5, 0.75]
            self.weights[2] = [1, 0.75, 0.5]

    def find_neighbors(self):
        # finds the weight neighbors of each weight equal. This consists of itself and n-1 others
        for weight_index, weight in enumerate(self.weights):
            distances = [0] * self.num_objectives
            for neigh_index, potential_neightbor in enumerate(self.weights):
                distances[neigh_index] = self.dist_between_weights(weight, potential_neightbor)
           #print(distances)
            for neighbor in range(self.num_neighbors):
                # get the weight vector that is closest to weight vector weight_index
                i_closest_vector = distances.index(min(distances))
                #print(i_closest_vector)
                self.neighbourhoods[weight_index][neighbor] = i_closest_vector
                # then set it to inf to keep the indexes the same and so it wont be assigned again
                distances[i_closest_vector] = inf
                #print(distances)
            print(self.neighbourhoods)

    def dist_between_weights(self, weightA, weightB):
        result = 0
        for i in range(self.num_objectives):
            result += (weightA[i] - weightB[i])**2
        return sqrt(result)
