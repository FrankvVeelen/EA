# Python script to run different EA algorithms on different problems. For now only TSP problem with MOEA/D


from problem_generation import Problem
from population import Population
from fitness import Fitness
from crossover import Crossover
from mutation import Mutation
from plotter import Plotter
from weights import Weights
from repair import Repair
from selection import Selection
from offspring import Offspring

from math import inf
import time
import random
import matplotlib.animation as animation
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
xdata, ydata = [], []
EP, = plt.plot([], [], 'ro', alpha=0.5)
# https://dces.essex.ac.uk/staff/qzhang/papers/moead.pdf

# settings
NUM_NODES = 20
SIZE_POPULATION = 500
NUM_WEIGHT_VECTORS = SIZE_POPULATION
NUM_OBJECTIVES = 2
NUM_NEIGHBORS = 10  # Called T in paper
GENERATIONS = 50
algorithm = "NSGA2"  # MOEA or NSGA2
mutation_type = "RSM"


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
mutation = Mutation("RSM", 0.05)  # 5% chance of mutation
repair = Repair()
weights = Weights(NUM_OBJECTIVES, NUM_WEIGHT_VECTORS, NUM_NEIGHBORS)
selection = Selection(population.population)
offspring_generator = Offspring()

start_time = time.time()

fitness.calculate_fitness_pop(population.population, problem)

if algorithm == "MOEA":
    fitness.calculate_z_optimums_pop()
elif algorithm == "NSGA2":
    selection.set_dominations(population.population)
    offspring_generator.generate_offspring(population.population, crossover, repair, SIZE_POPULATION, problem, fitness, mutation)


def init():
    ax.set_xlim(0, population.population[0].fitness[0]*NUM_OBJECTIVES)
    ax.set_ylim(0, population.population[0].fitness[1]*NUM_OBJECTIVES)
    return EP,

def step_MOEA():
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

def step_NSGA2():
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
    total_length = 0
    while len(new_population) + len(fronts[i]) < SIZE_POPULATION:
        selection.crowding_distance_assignment(fronts[i])
        for individual in fronts[i]:
            new_population.append(individual)
        i += 1
    if len(new_population) != SIZE_POPULATION:
        front = selection.sort_front(fronts[i])
        i = 0
        while len(new_population) < SIZE_POPULATION - 1:
            len(new_population)
            new_population.append(front[i])
            i += 1
    population.population = new_population

    x = []
    y = []
    for individual in population.population:
        x.append(individual.fitness[0])
        y.append(individual.fitness[1])
    EP.set_data(x, y)

    offspring_generator.generate_offspring(population.population, crossover, repair, SIZE_POPULATION, problem, fitness,
                                           mutation)
    return EP,
run_id = str(random.randint(0, 1000))
def run_problem(generation):
    print("Generation: " + str(generation))
    global start_time, algorithm, population

    if generation < GENERATIONS:
        algorithm = "MOEA"
        if algorithm == "MOEA":
            EP, = step_MOEA()
            return EP,
        else:
            EP, = step_NSGA2()
            return EP,
    elif generation == GENERATIONS:
        # save plot
        time_taken = (time.time() - start_time)
        print("EA done, ran for: " + str(generation) + " generations and for %.2f seconds" % time_taken)

        file_name = run_id + algorithm + "_G" + str(GENERATIONS) + "_N" + str(
            NUM_NODES) + "_P" + str(SIZE_POPULATION) + "_Ne" + str(NUM_NEIGHBORS) + "_T%d" % time_taken
        plt.savefig("plots/" + file_name)

        algorithm = "NSGA2"

        start_time = time.time()
        population = Population(SIZE_POPULATION, NUM_NODES, NUM_OBJECTIVES) # reset population
        fitness.calculate_fitness_pop(population.population, problem)

        if algorithm == "MOEA":
            fitness.calculate_z_optimums_pop()
        elif algorithm == "NSGA2":
            selection.set_dominations(population.population)
            offspring_generator.generate_offspring(population.population, crossover, repair, SIZE_POPULATION, problem,
                                                   fitness, mutation)
        EP, = step_NSGA2()
        return EP,
    elif generation < GENERATIONS*2:
        EP, = step_NSGA2()
        return EP,
    else:
        time_taken = (time.time() - start_time)
        print("EA done, ran for: " + str(generation) + " generations and for %d seconds" % time_taken)
        file_name = run_id + algorithm + "_G" + str(GENERATIONS) + "_N" + str(
            NUM_NODES) + "_P" + str(SIZE_POPULATION) + "_Ne" + str(NUM_NEIGHBORS) + "_T%d" % time_taken
        plt.savefig("plots/"+file_name)

        while True:
            time.sleep(100)

ani = animation.FuncAnimation(fig, run_problem, init_func=init, blit=True)
plt.show()

print("Final solutions: ")
for i in population.population:
    print(i.genotype)

