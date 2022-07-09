class Cromosome:
    def __init__(self, path, TSP):
        self.TSP = TSP
        self.path = path
        self.compute_cost()
        self.probability = 0

    def compute_cost(self):
        self.cost = 0
        for i in range(len(self.path) -1):    
            self.cost += self.TSP.get_weight(self.path[i-1],self.path[i])
        self.cost += self.TSP.get_weight(self.path[0-1],self.path[0])
        self.cost = 1 / self.cost

    def set_probability(self, prob):
        self.probability = prob

    def get_path(self):
        return self.path

    def get_cost(self):
        return self.cost

    def get_probability(self):
        return self.probability

    def __len__(self):
        return len(self.path)

    def __str__(self):
        return f'{self.path}: {int(1/self.cost)}'

    def __add__(self, x):
        if type(x) == int or type(x) == float:
            return self.cost + x
        else:
            return self.cost + x.cost

    def __radd__(self, x):
        if type(x) == int or type(x) == float:
            return self.cost + x
        else:
            return self.cost + x.cost
        
    def __lt__(self, x):
        if self.cost < x.cost:
            return True
        else:
            return False

    def __le__(self, x):
        if self.cost <= x.cost:
            return True
        else:
            return False

    def __gt__(self, x):
        if self.cost > x.cost:
            return True
        else:
            return False
    
    def __ge__(self, x):
        if self.cost >= x.cost:
            return True
        else:
            return False
