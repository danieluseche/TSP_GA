from random import choice, random, randint
from math import sqrt
import tsplib95
import csv
from cromosome import Cromosome
from crossover import PMX_crossover
from mutation import swap_mutation

class Genetic:
    def __init__(self, TSP_file, population = 10, generations = 10, output_file = 'output_file.csv'):
        self.max_generations = generations

        self.output_file = output_file
        #Star with a empty file:
        with open(output_file, 'r+') as f:
            f.truncate()

        #Cargar Problema
        self.TSP = self.tsp_load(TSP_file)
        self.population = [None for x in range(population)]

        self.new_generation = []
        self.generation_sum_cost = 0

        self.cumulative_probs = []

        self.mutation_rate = 0.3
        self.crossover_rate = 0.7
        self.best_individual = Cromosome([0,1],self.TSP)
        self.best_individual.cost = 0

    def __str__(self):
        return f'\n'.join([str(individual) for individual in self.population])

    def tsp_load(self, TSP_file):
        with open(TSP_file):
            return tsplib95.load(TSP_file)
    
    def write_costs_to_file(self):
        with open(self.output_file, mode='a') as csv_file:
            writer = csv.writer(csv_file, delimiter = ',')
            writer.writerow([round(1 / individual.get_cost()) for individual in self.population])

    def populate(self):
        for i in range(len(self.population)):
            path = [0]
            opt = [x for x in range(1, self.TSP.dimension)]
            while len(path) != self.TSP.dimension:
                num = choice(opt)
                path.append(num)
                opt.remove(num)

            self.population[i] = Cromosome(path, self.TSP)
        self.compute_generation_cost()

    def populate_from_file(self, file_name):
        with open(file_name) as csv_file:
            csv_reader = csv.reader(csv_file)
            list_of_csv = list(csv_reader)
        self.population = [Cromosome([int(item) for item in ind], self.TSP) for ind in list_of_csv]
        self.compute_generation_cost()


    def compute_generation_cost(self):
        self.generation_sum_cost = sum(self.population)

        #Valor promedio de la generación:
        self.generation_prom = self.generation_sum_cost / len(self.population)

        #Desviacion Estandar:
        tmp = [ (x.get_cost() - self.generation_prom)**2 for x in self.population]
        self.standard_deviation = sqrt(sum(tmp)/len(self.population))

        #Organizar la población:
        self.population = sorted(self.population)
        self.find_best_individual()        

    def find_best_individual(self):
        if self.population[-1] >= self.best_individual:
            self.best_individual = self.population[-1]

    def compute_generation_probability(self):
        self.cumulative_probs = []

        for individual in self.population:        
            individual.set_probability(individual.get_cost()/self.generation_sum_cost)

            if self.population.index(individual) == 0:
                self.cumulative_probs.append(individual.get_probability())
            else:
                self.cumulative_probs.append(\
                        individual.get_probability() + \
                        self.cumulative_probs[self.population.index(individual)-1])

    def print_prob_table(self):
        print('  i        cost    prob     cum  N°') 

        for individual, cum_prob in zip(self.population, self.cumulative_probs):
            print(f'{self.population.index(individual):3d}: {individual.cost:.4e} {individual.get_probability()*100:6.2f}% {cum_prob*100:6.2f}%  {round(individual.get_probability()*len(self.population))}')
        print(f'  Prom: {self.generation_prom:.4e} SD: {self.standard_deviation:.4e}')

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
        if self.population[-1].cost > 20 * self.standard_deviation:
            if self.population[-1] not in self.new_generation:
                self.new_generation.append(self.population[-1])

    def run(self):
        #If there is no population take a random one
        if None in self.population:
            self.populate()

        for generation in range(self.max_generations):

            #Prepare the actual population:
            self.compute_generation_cost()
            self.compute_generation_probability()
            #self.print_prob_table()
            
            #write to file:
            self.write_costs_to_file()

            #Fill the new generation:
            while len(self.new_generation) != len(self.population):
                 
                #self.elitism()

                if random() < self.crossover_rate:
                    cross_path = []
                    n1 = 0
                    n2 = 0
                    while n1 == n2:
                        n1 = self.roulette_selection()
                        n2 = self.roulette_selection()
                    cross_path = PMX_crossover(self.population[n1].get_path(),self.population[n2].get_path())

                    self.new_generation.append(Cromosome(cross_path, self.TSP))
                    continue

                if random() < self.mutation_rate:
                    mutated_path = swap_mutation(self.population[self.roulette_selection()].get_path())
                    self.new_generation.append(Cromosome(mutated_path, self.TSP))
                    continue

            self.population = self.new_generation.copy()
            self.new_generation.clear()

        return self.best_individual


if __name__=='__main__':
    problem = Genetic('gr21.tsp', population = 20, generations = 20)
    print(problem.run())
    # Random first generation
    # problem.populate() 
    
    # Search among generations a better solution
    # while True:
    #     problem.populate()
    #     print(f'{problem.population[0].cost}:{problem.population[0].path}')
    #     if problem.population[0].cost < 4000:
    #         break
    
    #problem.populate_from_file('population.csv')
    #print(problem)

    #GENERATIONS LOOP
    #selection
    # problem.compute_generation_probability()
    # problem.print_prob_table()


#***************************FIND BEST*****************************************************
    # print('best individual:')
    # print(problem.best_individual)


#***************************SELECTION*****************************************************
    # print(problem.roulette_selection())

#***************************ELITISM*******************************************************
    # print('elitism:')
    # problem.elitism()

#***************************MUTATION*******************************************************
    # print('before:')
    # print(problem.best_individual.get_path())
    # print('after:')
    # print(swap_mutation(problem.best_individual.path))

#***************************CROSSOVER*******************************************************
    # n1 = 0
    # n2 = 0
    # while n1 == n2:
    #     n1 = problem.roulette_selection()
    #     n2 = problem.roulette_selection()
    # print('Chosen:')
    # print(problem.population[n1])
    # print(problem.population[n2])
    # print('Child:')
    # print(PMX_crossover(problem.population[n1].get_path(),problem.population[n2].get_path()))

 #*****************************************************************************************   

  
