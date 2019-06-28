# Python script to run different EA algorithms on different problems. For now only TSP problem with MOEA/D


from problem_generation import Problem
from population import Population
from fitness import Fitness
from crossover import Crossover
from plotter import Plotter
from weights import Weights
from repair import Repair
import time
from math import inf
import matplotlib.animation as animation
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
xdata, ydata = [], []
EP, = plt.plot([], [], 'ro')
# https://dces.essex.ac.uk/staff/qzhang/papers/moead.pdf

# settings
NUM_NODES = 10
NUM_WEIGHT_VECTORS = 100
NUM_OBJECTIVES = 2
NUM_NEIGHBORS = 25  # Called T in paper
SIZE_POPULATION = NUM_WEIGHT_VECTORS
GENERATIONS = 3


def gte(genotype_fitness, neighbour):
    min_result = inf
    for i in range(NUM_OBJECTIVES):
        if weights.weights[neighbour][i]*abs(genotype_fitness[i] - fitness.z_optimum[i]) < min_result:
            min_result = weights.weights[neighbour][i] * abs(genotype_fitness[i] - fitness.z_optimum[i])
    return min_result


# generate a problem
weights = Weights(NUM_OBJECTIVES, NUM_WEIGHT_VECTORS, NUM_NEIGHBORS)
problem = Problem("TSP", NUM_OBJECTIVES, weights.weights, NUM_NODES, NUM_NEIGHBORS)
# generate an initial population
population = Population(SIZE_POPULATION, NUM_NODES)
# calculate initial fitness
fitness = Fitness("MO_tsp", SIZE_POPULATION, NUM_OBJECTIVES, weights.weights)
# create crossover object to be used later
crossover = Crossover("Order")
repair = Repair()

fitness.calculate_fitness_pop(population.population, problem)
fitness.calculate_z_optimums_pop()

def init():
    ax.set_xlim(0, 50000)
    ax.set_ylim(0, 50000)
    return EP,

def run_problem(generation):
    print("Generation: " + str(generation))
    for i_neighbourhood, neighbourhood in enumerate(weights.neighbourhoods):
        # Reproduction
        child = crossover.reproduce(neighbourhood, population.population)
        # Calculate fitness of child
        child_fitness = fitness.calculate_fitness_genotype(child, problem)
        # Improvement
        [child, child_fitness] = repair.get_new_child(SIZE_POPULATION, problem, child, child_fitness, fitness)
        # print(str(child) + str(child_fitness))
        # update of z
        fitness.calculate_z_optimums_genotype(child_fitness)
        # update of neighboring solutions
        for j, neighbour in enumerate(neighbourhood):
            if gte(child_fitness, neighbour) < gte(fitness.fitnesses[neighbour][:], neighbour):
                population.population[neighbour] = child
                fitness.fitnesses[neighbour][:] = child_fitness
                #print("Genotype was replaced")
                break
        # update of EP
        population.remove_dominated_EP_by_child(child_fitness)
        population.add_to_elite(child, child_fitness)
        #for elite_fitness in population.elite_fitnesses:
            #print(elite_fitness)
        x, y = zip(*population.elite_fitnesses)
        EP.set_data(x, y)
        return EP,


ani = animation.FuncAnimation(fig, run_problem, init_func=init, interval=2, blit=True, save_count=50)
plt.show()

# plotter = Plotter()
#
# plotter.plotRoute(problem, population.elite_population[0], 0)
# plotter.plotRoute(problem, population.elite_population[0], 1)

