from random import choice, random, randint
import tsplib95
import csv
from cromosome import Cromosome
from crosover import *

class Genetic:
    def __init__(self, TSP_file, population=20, generations = 20):
        self.generation_count = 20
        #Cargar Problema
        self.TSP = self.tsp_load(TSP_file)
        self.population = [Cromosome([0]) for x in range(population)]
        self.new_generation = []
        self.generation_sum_cost = 0

        self.individual_probs = []
        self.cumulative_probs = []

        self.mutation_rate = 0.3
        self.crossover_rate = 0.7
        self.best_individual = Cromosome()

    def __str__(self):
        return f'\n'.join([str(individual) for individual in self.population])

    def tsp_load(self, TSP_file):
        with open(TSP_file):
            return tsplib95.load(TSP_file)

    def populate(self):
        self.population = [Cromosome([0]) for x in range(len(self.population))]
        for individual in self.population:
            opt = [x for x in range(1, self.TSP.dimension)]
            while len(individual.path) != 21:
                num = choice(opt)
                individual.path.append(num)
                opt.remove(num)

        self.compute_generation_cost()

    def populate_from_file(self, file_name):
        with open(file_name) as csv_file:
            csv_reader = csv.reader(csv_file)
            list_of_csv = list(csv_reader)
        self.population = [Cromosome([int(item) for item in ind]) for ind in list_of_csv]
        self.compute_generation_cost()

    def find_best_individual(self):
        if self.population[-1] >= self.best_individual:
            self.best_individual = self.population[-1]

    def compute_cost(self, individual):
            cost = 0
            for i in range(self.TSP.dimension - 1):
                cost += self.TSP.get_weight(individual.path[i], individual.path[i+1])
            cost += self.TSP.get_weight(individual.path[-1], individual.path[0])
            return cost

    def compute_generation_cost(self):
        self.generation_sum_cost = 0
        for individual in self.population:
            #Due to minimization, we must invert the cost function
            individual.cost = 1/self.compute_cost(individual)
            self.generation_sum_cost += individual.cost
        
        self.population = sorted(self.population)
        self.find_best_individual()        


    def compute_generation_probability(self):
        self.individual_probs = []
        self.cumulative_probs = []

        for individual in self.population:        
            self.individual_probs.append(individual.cost/self.generation_sum_cost)
            
            if self.population.index(individual) == 0:
                self.cumulative_probs.append(self.individual_probs[self.population.index(individual)])
            else:
                self.cumulative_probs.append(self.individual_probs[self.population.index(individual)] + self.cumulative_probs[self.population.index(individual)-1])

    def print_prob_table(self):
        print('  i        cost    prob     cum  N°') 

        for individual, prob, cum_prob in zip(self.population, self.individual_probs, self.cumulative_probs):
            print(f'{self.population.index(individual):3d}: {individual.cost:.4e} {prob*100:6.2f}% {cum_prob*100:6.2f}%  {round(prob*len(self.population))}')

    def binary_search(self, num, init, end):
        if end >= init:
            
            mid_point = (init + end) // 2

            if self.cumulative_probs[mid_point] >= num and self.cumulative_probs[mid_point - 1] < num:
                return mid_point
            elif self.cumulative_probs[mid_point] > num and mid_point == 1:
                return mid_point
            elif self.cumulative_probs[mid_point] > num:
                return self.binary_search(num, init, mid_point - 1)
            elif self.cumulative_probs[mid_point] < num:
                return self.binary_search(num, mid_point + 1, end)
        else:
            return False

    def roulette_selection(self):
        return self.binary_search(random(), init = 0, end = len(problem.population) - 1)
    
    def elitism(self):
        if self.population[-1] > 5 / len(self.population):
            self.new_generation.append(self.population[-1])

    def swap_mutation(self,individual):
        mutated_path = individual.path.copy()
        n1 = randint(0, len(individual.path))
        n2 = randint(0, len(individual.path))
        mutated_path[n1] = individual.path[n2]
        mutated.path[n2] = individual.path[n1]
        return Cromosome(mutated_path)
        
    def run(self):
        #for generation in range(self.generation_count):
        self.compute_generation_cost()
        self.compute_generation_probability()  

        while len(self.new_generation) != len(self.population): 
            #Selection
            self.elitism()
            
            #Crossover
            if random() < self.crossover_rate:
                p1 = 0
                p2 = 0
                while p1 == p2:
                    p1 = roulette_selection()
                    p2 = roulette_selection()
                self.new_generation.append(cycle_crossover(self.population[p1], self.population[p2]))

            #Mutation
            if random() < self.mutation_rate:
                self.new_generation.append(self.swap_mutation(), self.population[self.roulette_selection()])

        self.population = self.new_generation.copy()
        self.new_generation = []


if __name__=='__main__':
    problem = Genetic('gr21.tsp', 10)
    
    # Random first generation
    problem.populate()
    
    # Search among generations a better solution
    # while True:
    #     problem.populate()
    #     print(f'{problem.population[0].cost}:{problem.population[0].path}')
    #     if problem.population[0].cost < 4000:
    #         break
    
    #problem.populate_from_file('population.csv')
    #print(problem)

    #Asignando un valor de costo bajo
    # problem.population[0].cost = 1/4000
    # problem.generation_sum_cost=0
    # for individual in problem.population:
    #     problem.generation_sum_cost += individual.cost

    #GENERATIONS LOOP
    #selection
    problem.compute_generation_probability()
    problem.print_prob_table()
    #trow a random number
    
    #Populate NEW GENERATION
    #print(problem.roulette_selection())
    print(problem.best_individual)
    #recombination

    #Mutation

  
