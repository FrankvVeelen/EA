# Python script to run different EA algorithms on different problems. For now only TSP problem with MOEA/D


from problem_generation import Problem
from population import Population
from fitness import Fitness
from crossover import Crossover
from plotter import Plotter
from weights import Weights
import time
from math import inf
import matplotlib.animation as animation
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'ro')
# https://dces.essex.ac.uk/staff/qzhang/papers/moead.pdf

# settings
NUM_NODES = 10
NUM_OBJECTIVES = 2
NUM_NEIGHBORS = 2  # Called T in paper
SIZE_POPULATION = NUM_OBJECTIVES
GENERATIONS = 3


def gte(genotype_fitness, j):
    min_result = inf
    for i in range(NUM_OBJECTIVES):
        if weights.weights[i][j]*abs(genotype_fitness[i] - fitness.best_genotype_1d[i]) < min_result:
            min_result = weights.weights[j][i]*abs(genotype_fitness[i] - fitness.best_genotype_1d[i])
    return min_result

# generate a problem
weights = Weights(NUM_OBJECTIVES, NUM_NEIGHBORS)
problem = Problem("TSP", NUM_OBJECTIVES, weights.weights, NUM_NODES, NUM_NEIGHBORS)
# generate an initial population
population = Population(SIZE_POPULATION, NUM_NODES)
# calculate initial fitness
fitness = Fitness("MO_tsp", SIZE_POPULATION, NUM_OBJECTIVES, weights.weights)
# create crossover object to be used later
crossover = Crossover("Order")

fitness.calculate_fitness_pop(population.population, problem)
fitness.calculate_z_optimums_pop()

def init():
    ax.set_xlim(0, 10000)
    ax.set_ylim(0, 10000)
    return ln,

def run_problem(generation):
    print("Generation: " + str(generation))
    for i_neighbourhood, neighbourhood in enumerate(weights.neighbourhoods):
        # Reproduction
        child = crossover.reproduce(neighbourhood, population.population)
        # Calculate fitness of child
        child_fitness = fitness.calculate_fitness_genotype(child, problem)
        # Improvement
        # to be implemented, maybe random switch of cities?
        # update of z
        fitness.calculate_z_optimums_genotype(child_fitness)
        # update of neighboring solutions
        for j, neighbour in enumerate(neighbourhood):
            if gte(child_fitness, j) < gte(fitness.fitnesses[:][j], j):
                population.population[j] = child
                fitness.fitnesses[:][j] = child_fitness
                print("Genotype was replaced")
                break
        # update of EP
        population.remove_dominated_EP_by_child(child_fitness, NUM_OBJECTIVES)
        population.add_to_elite(child, child_fitness, NUM_OBJECTIVES)
        print(population.elite_fitnesses)
        x, y = zip(*population.elite_fitnesses)
    ln.set_data(x, y)
    time.sleep(1)
    return ln,


ani = animation.FuncAnimation(fig, run_problem, init_func=init, interval=2, blit=True, save_count=50)
plt.show()

