# TSPGA
### Genetic algorithm to solve TSP problems

Solving the the [travelling salesman problem](https://en.wikipedia.org/wiki/Travelling_salesman_problem) (TSP) with a 
[genetic algorithm](https://en.wikipedia.org/wiki/Genetic_algorithm) (GA). With the 
[initial data set](https://github.com/EvilScott/tspga/blob/master/data/western_sahara.py) the results have been very good:
```bash
$ time python tspga.py 
best after 250 gens: 27748; optimal: 27603; delta: 145 (99.5%)

real	0m5.351s
user	0m5.334s
sys	0m0.012s
```

- More data sets are available [here](http://www.math.uwaterloo.ca/tsp/world/countries.html).
- To edit values used for the algorithm, edit the constants found [here](https://github.com/EvilScott/tspga/blob/master/values.py).
