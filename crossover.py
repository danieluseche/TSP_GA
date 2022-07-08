from random import randint

def to_index_notation(p):
    p_mod = []
    for i in range(len(p)):
        if p.index(i) == len(p)-1:
            p_mod.append(0)
        else:
            p_mod.append(p[p.index(i)+1])
    return p_mod

def to_path_notation(p):
    path= []
    for i in range(len(p)):
        if i == 0:
            path.append(0)
        else:
            path.append(p[path[i-1]])
    return path

def find_cycles(p1, p2):
    unused_index = sorted(p1, reverse = True)
    num_of_cycles = 0
    cycles = []
    while len(unused_index):    
        index = unused_index.pop()
        init = p1[index]
        p = -1
        cycles.append([])
        while p != init:
            if p == -1:
                cycles[num_of_cycles].append(init)
            else:
                cycles[num_of_cycles].append(p)
                unused_index.remove(index)
            index = p1.index(p2[index])
            
            p = p1[index]
        num_of_cycles += 1
    return cycles

def cycle_crossover(p1, p2):
    p1_mod = to_index_notation(p1)
    p2_mod = to_index_notation(p2)

    cycles = find_cycles(p1_mod, p2_mod)
    child = [0 for i in range(len(p1))]
    for i, cycle in enumerate(cycles, start = 1):
        
        print(f'cycle {i}: {cycle}')
        for item in cycle:
            if i % 2 == 0:
                child[p2_mod.index(item)] = item
            else:
                child[p1_mod.index(item)] = item

        if i % 2 == 0:
            print(p2_mod)
        else:
            print(p1_mod)
        print(child)
    return to_path_notation(child)

def slice_parent(p):
    init = 0
    end = 0
    while init >= end:
        init = randint(0,len(p)-1)
        end = randint(0,len(p)-1)
    return p[init:end]

def PMX_crossover(p1, p2):
    child = slice_parent(p1)
    for item in p2:
        if item not in child:
            child.append(item)

    print(child)
    if child[0] != 0:
        tmp = []
        for item in child[0:child.index(0)]:
            child.remove(item)
            child.append(item)
    return child

if __name__ == '__main__':
    p1 = [0, 9, 7, 12, 4, 14, 2, 11, 16, 5, 20, 8, 6, 17, 3, 10, 13, 18, 15, 1, 19]
    p2 = [0, 12, 5, 13, 11, 4, 19, 15, 14, 7, 1, 18, 2, 6, 9, 10, 20, 17, 3, 8, 16]
    
    print()
    print(PMX_crossover(p1,p2))
