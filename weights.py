from math import sqrt, inf


class Weights:
    def __init__(self, num_obj, num_weights, num_neighbors):
        self.num_objectives = num_obj
        self.num_neighbors = num_neighbors
        self.num_weights = num_weights
        self.weights = [0] * num_weights
        self.generate_objective_weights()
        self.neighbourhoods = [0] * num_weights  #neighbours for weight[i] are itself and the closest weight vectors
        for i in range(num_weights):
            self.neighbourhoods[i] = [0] * num_neighbors
        self.find_neighbors()

    def generate_objective_weights(self):
        # https: // thiagodnf.github.io / weight - vectors - generator /
        if self.num_objectives == 2:
            self.weights[0] = [1, 0]
            for i in range(1, self.num_weights):
                self.weights[i] = [1 - (1/self.num_weights)*i, 0+(1/self.num_weights)*i]
            print(self.weights)
        elif self.num_objectives == 3:
            self.weights[0] = [0.5, 0.75, 1]
            self.weights[1] = [1, 0.5, 0.75]
            self.weights[2] = [1, 0.75, 0.5]

    def find_neighbors(self):
        # finds the weight neighbors of each weight equal. This consists of itself and n-1 others
        for weight_index, weight in enumerate(self.weights):
            distances = [0] * self.num_weights
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
