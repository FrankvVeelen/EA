import random

class Repair:
	def swap_child_gene(self, child, i, n):
		swap = child[i]
		child[i] = child[n]
		child[n] = swap
		return child

	def get_new_child(self, max_exchanges, problem, child, fitness):
		N = random.randint(0, len(child)-1)
		num_exchanges = 0
		new_fitness = 0
		current_fitness = fitness.calculate_fitness_genotype(child, problem)

		for i in range(N, len(child)-1):
			for n in range(i+1, len(child)-1):
				# check whether maximum number of exchanges allowed is reached
				# if max_exchanges = -1 (no limit), keep running untill no exchanges possible
				if max_exchanges < 0 or max_exchanges > num_exchanges:
					# swap current gene with i+1 (in beginning its N+1)
					child = swap_child_gene(child, i, n)

					# check whether new child has a better fitness (thus lower) than original child
					new_fitness = fitness.calculate_fitness_genotype(child, problem)
					if current_fitness > new_fitness:
						# if fitness is better, increment num_exchanges and break as we dont need to check further in this loop
						num_exchanges += 1
						break
					else:
						# if fitness is worse, swap back 
						child = swap_child_gene(child, i, n)
			
				else:
					break