from random import randint
def swap_mutation(individual):
    mutated_path = individual.copy()
    n1 = 0
    n2 = 0
    while n1 == n2:
        n1 = randint(0, len(individual) -1)
        n2 = randint(0, len(individual) -1)
        
    mutated_path[n1] = individual[n2]
    mutated_path[n2] = individual[n1]
    return mutated_path

if __name__ == '__main__':
    p1 = [0, 9, 7, 12, 4, 14, 2, 11, 16, 5, 20, 8, 6, 17, 3, 10, 13, 18, 15, 1, 19]
    print(p1)
    print(swap_mutation(p1))