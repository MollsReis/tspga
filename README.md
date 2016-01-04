# TSPGA
### Genetic algorithm to solve TSP problems

Solving the the [travelling salesman problem](https://en.wikipedia.org/wiki/Travelling_salesman_problem) (TSP) with a 
[genetic algorithm](https://en.wikipedia.org/wiki/Genetic_algorithm) (GA). With the 
[initial data set](https://github.com/EvilScott/tspga/blob/master/data/western_sahara.py) the results have been very good:
```bash
$ time python tspga.py 
best after 250 gens: 28869; optimal: 27603; delta: 1266 (95.4%)

real	0m6.378s
user	0m6.254s
sys	0m0.049s
```

- More data sets are available [here](http://www.math.uwaterloo.ca/tsp/world/countries.html).
- To edit values used for the algorithm, edit the constants found [here](https://github.com/EvilScott/tspga/blob/master/values.py).
