def a_dominates_b(fitness_a, fitness_b):
    flag = False
    num_objectives = len(fitness_a)
    objectives_dominated = 0
    for i in range(num_objectives):
        if fitness_a[i] <= fitness_b[i]:
            objectives_dominated += 1
    # print("Count: " + str(domination_count) + "Thres: " + str(len(elite_fitness)))
    if objectives_dominated == num_objectives:
        flag = True
        # print("not adding to EP")
    return flag
