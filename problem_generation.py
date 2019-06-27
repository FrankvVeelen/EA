import random
import numpy as np
from math import hypot

class Problem:
    def __init__(self, problem_type, num_objectives, objective_weights, num_nodes, num_neighbors):
        self.type = problem_type
        self.num_objectives = num_objectives
        self.objective_weights = objective_weights
        self.num_nodes = num_nodes
        self.num_neighbors = num_neighbors
        if self.type == "TSP":
            self.nodes = self.TSP(self.num_objectives, self.num_nodes)
        # self.calculate_neighbors()

    def TSP(self, num_obj, num_nodes):
        nodes = [None] * num_nodes
        for node in range(0, num_nodes): # for number of nodes wanted
            for obj in range(0, num_obj): # for each objective
                x = get_random_dist(num_obj)
                y = get_random_dist(num_obj)
                nodes[node] = Node(node, x, y)
        return nodes

    # def calculate_neighbors(self):
    #     for node in self.nodes:
    #         for other_node in self.nodes:
    #             node.distances[other_node.number] = distance_between_nodes(node, other_node, self.num_objectives, self.objective_weights)
    #
    #     for node in self.nodes:
    #         tempNodeList = self.nodes
    #         tempNodeList.sort()


class Node:  # store x[num_obj] and y[num_obj] arrays
    def __init__(self, number, x, y):
        self.number = number
        self.x = x
        self.y = y


def get_random_dist(num_obj):
    # can add different distributions for different objectives here
    # weight_distributions = [0, 100]
    dist = [None] * num_obj
    for obj in range(0, num_obj):
        dist[obj] = random.randint(0, 100)
    return dist

