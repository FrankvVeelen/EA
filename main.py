# Python script to run different EA algorithms on different problems. For now only TSP problem with MOEA/D


from problem_generation import Problem
from population import Population
from fitness import Fitness
from crossover import Crossover
from plotter import Plotter
from weights import Weights
from repair import Repair
from selection import Selection
from offspring import Offspring

from math import inf
import matplotlib.animation as animation
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
xdata, ydata = [], []
EP, = plt.plot([], [], 'ro', alpha=0.5)
# https://dces.essex.ac.uk/staff/qzhang/papers/moead.pdf

# settings
NUM_NODES = 50
NUM_WEIGHT_VECTORS = 20
NUM_OBJECTIVES = 2
NUM_NEIGHBORS = 3  # Called T in paper
SIZE_POPULATION = NUM_WEIGHT_VECTORS
GENERATIONS = 3
algorithm = "NSGA2"


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
crossover = Crossover("Order")
repair = Repair()
if algorithm == "MOEA":
    weights = Weights(NUM_OBJECTIVES, NUM_WEIGHT_VECTORS, NUM_NEIGHBORS)
elif algorithm == "NSGA2":
    selection = Selection(population.population)
    offspring_generator = Offspring()

fitness.calculate_fitness_pop(population.population, problem)

if algorithm == "MOEA":
    fitness.calculate_z_optimums_pop()
elif algorithm == "NSGA2":
    selection.set_dominations(population.population)
    offspring_generator.generate_offspring(population.population, crossover, repair, SIZE_POPULATION, problem, fitness)


def init():
    ax.set_xlim(0, population.population[0].fitness[0]*NUM_OBJECTIVES)
    ax.set_ylim(0, population.population[0].fitness[1]*NUM_OBJECTIVES)
    return EP,

def run_problem(generation):
    print("Generation: " + str(generation))
    if algorithm == "MOEA":
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
    else:
        selection.set_dominations(population.population)
        selection.sort_dominations(population.population)
        new_population = []
        i = 1
        fronts = []
        while sum(len(x) for x in fronts) < SIZE_POPULATION:
            front = selection.find_front(i, population.population)
            fronts.append(front)
            i += 1
        i = 0
        print("Fronts found:" + str(len(fronts)))
        print("fronts: " + str(fronts))
        total_length = 0
        print("Length front 1: " + str(len(fronts[i])))
        print("Front 1: " + str(fronts[i]))
        while len(new_population) + len(fronts[i]) < SIZE_POPULATION:
            print("front: " +str(i))
            #selection.crowding_distance_assignment(fronts[i])
            print("adding individual")
            for individual in fronts[i]:
                new_population.append(individual)
            i += 1
        if len(new_population) != SIZE_POPULATION:
            front = selection.sort_front(fronts[i])
            i = 0
            print("last front: " + str(front))
            while len(new_population) < SIZE_POPULATION-1:
                len(new_population)
                print(i)
                new_population.append(front[i])
                i += 1
        print("size new population: " + str(len(new_population)))
        population.population = new_population

        x = []
        y = []
        for individual in population.population:
            print(individual.fitness)
            x.append(individual.fitness[0])
            y.append(individual.fitness[1])
        EP.set_data(x, y)

        offspring_generator.generate_offspring(population.population, crossover, repair, SIZE_POPULATION, problem, fitness)
        for individual in population.population:
            print(individual.fitness)
        return EP,


ani = animation.FuncAnimation(fig, run_problem, init_func=init, interval=2, blit=True, save_count=50)
plt.show()
#
# plotter = Plotter()
#
# plotter.plotRoute(problem, population.elite_population[0], 0)
# plotter.plotRoute(problem, population.elite_population[0], 1)

