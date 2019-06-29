# Python script to run different EA algorithms on different problems. For now only TSP problem with MOEA/D


from problem_generation import Problem
from population import Population
from fitness import Fitness
from crossover import Crossover
from plotter import Plotter
from weights import Weights
from repair import Repair
from selection import Selection

from math import inf
import matplotlib.animation as animation
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
xdata, ydata = [], []
EP, = plt.plot([], [], 'ro', alpha=0.5)
# https://dces.essex.ac.uk/staff/qzhang/papers/moead.pdf

# settings
NUM_NODES = 50
NUM_WEIGHT_VECTORS = 100
NUM_OBJECTIVES = 2
NUM_NEIGHBORS = 30  # Called T in paper
SIZE_POPULATION = NUM_WEIGHT_VECTORS
GENERATIONS = 3
algorithm = "MOEA"


def gte(genotype_fitness, neighbour):
    min_result = inf
    for i in range(NUM_OBJECTIVES):
        if weights.weights[neighbour][i]*abs(genotype_fitness[i] - fitness.z_optimum[i]) < min_result:
            min_result = weights.weights[neighbour][i] * abs(genotype_fitness[i] - fitness.z_optimum[i])
    return min_result


problem = Problem("TSP", NUM_OBJECTIVES, NUM_NODES)
# generate an initial population
population = Population(SIZE_POPULATION, NUM_NODES, NUM_OBJECTIVES)
# calculate initial fitness
fitness = Fitness("MO_tsp", SIZE_POPULATION, NUM_OBJECTIVES, population.population)
# create crossover object to be used later
# generate a problem
if algorithm == "MOEA":
    crossover = Crossover("Order")
    weights = Weights(NUM_OBJECTIVES, NUM_WEIGHT_VECTORS, NUM_NEIGHBORS)
    repair = Repair()
elif algorithm == "NSGA2":
    selection = Selection(SIZE_POPULATION)
    offspring_generator = Offspring()
    pass

fitness.calculate_fitness_pop(population.population, problem)
fitness.calculate_z_optimums_pop()

def init():
    ax.set_xlim(0, population.population[0].fitness[0]*NUM_OBJECTIVES)
    ax.set_ylim(0, population.population[0].fitness[1]*NUM_OBJECTIVES)
    return EP,

def run_problem(generation):
    print("Generation: " + str(generation))
    for neighbourhood in weights.neighbourhoods:
        # Reproduction
        child = crossover.reproduce(neighbourhood, population.population)
        # Calculate fitness of child
        child_fitness = fitness.calculate_fitness_genotype(child, problem)
        # Improvement
        [child, child_fitness] = repair.get_new_child(SIZE_POPULATION, problem, child, child_fitness, fitness)
        # update of z
        fitness.calculate_z_optimums_genotype(child_fitness)
        # update of neighboring solutions
        for neighbour in neighbourhood:
            if gte(child_fitness, neighbour) < gte(population.population[neighbour].fitness, neighbour):
                population.population[neighbour].genotype = child
                population.population[neighbour].fitness = child_fitness
                break
        # update of EP
        population.add_to_elite(child, child_fitness)
    x, y = zip(*population.elite_fitnesses)
    print("Number of elite solutions: " + str(len(x)))
    EP.set_data(x, y)
    return EP,


ani = animation.FuncAnimation(fig, run_problem, init_func=init, interval=2, blit=True, save_count=50)
plt.show()

plotter = Plotter()

plotter.plotRoute(problem, population.elite_population[0], 0)
plotter.plotRoute(problem, population.elite_population[0], 1)

