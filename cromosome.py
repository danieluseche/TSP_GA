class Cromosome:
    def __init__(self, path=[], cost=0):
        self.path = path
        self.cost = cost

    def __str__(self):
        return str(self.path)

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
