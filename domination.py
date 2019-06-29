def a_dominates_b(fitness_a, fitness_b):
    flag = False
    num_objectives = len(fitness_a)
    domination_count = 0
    for i in range(num_objectives):
        if fitness_a[i] <= fitness_b[i]:
            domination_count += 1
    # print("Count: " + str(domination_count) + "Thres: " + str(len(elite_fitness)))
    if domination_count == num_objectives:
        flag = True
        # print("not adding to EP")
    return flag
