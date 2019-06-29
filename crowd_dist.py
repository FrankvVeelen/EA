import math

def crowding_distance_assignment(I):
	l = len(I)
	I_dist = [0] * l

	for m in range(len(I.fitness))
		I.sort(key=lambda population: population.fitness[m])
		I_dist[0] = I_dist[l-1] = math.inf
		
		for i in range(1, l-2)
			I_dist[i] = I_dist[i] + (I[i+1].fitness[m] - I[i-1].fitness[m])/(I[i].fitness[-1] - I[i].fitness[0])
