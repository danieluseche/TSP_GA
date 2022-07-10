# TSP_GA
genetic algorithms aplied to travel salesman problem

##Code:
~~~
problem = Genetic('gr21.tsp', population = 20, generations = 20)
print(f'best solution:')
print(problem.run())
~~~

##Output example:
best solution:
[0, 15, 4, 5, 7, 6, 11, 3, 10, 12, 13, 14, 1, 20, 16, 9, 17, 19, 8, 2, 18]: 3771

##output Image:
![Generations Heatmap](https://github.com/danieluseche/TSP_GA/blob/main/evolution.svg)