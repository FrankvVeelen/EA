import matplotlib.pyplot as plt # for plotting
import matplotlib.animation as animation

class Plotter():
    #def __init__(self, problem, genotype, objective):
        #self.plotRoute(problem, genotype, objective)
        #plt.show()
    def plotRoute(self, problem, genotype, objective):
        # previousCity = population.population[genotype][NUM_NODES-1]  # to make it cyclical, otherwise make None
        previousCity = None
        for city in genotype:
            if previousCity is not None:
                plt.plot([problem.nodes[previousCity].x[objective], problem.nodes[city].x[objective]],
                         [problem.nodes[previousCity].y[objective], problem.nodes[city].y[objective]],
                         linestyle='dashed', linewidth=2)
            previousCity = city

        for node in problem.nodes:
            plt.plot(node.x[objective], node.y[objective], 'ro')
        plt.show()