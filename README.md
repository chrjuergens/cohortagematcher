# Cohort Age Matching

This repository provides a python package that computes an age-optimized matching between entities of two disjoint groups.
The underlying combinatorial optimization problem is called [assignment problem](https://en.wikipedia.org/wiki/Assignment_problem) which can be formulated in terms of graph theory:
> The assignment problem consists of finding, in a weighted bipartite graph, a matching of maximum size, in which the sum of weights of the edges is minimum.

## Use case: patients and controls

Consider two groups, a patient group and a control group.
We call individual entitites **patients** and **controls**. 
The goal is to find a matching between patients and controls so that the sum of age differences is minimal.

### Conditions

- Each patient must be assigned to a control.
- The matching can be restricted to gender.

### Remark

The package [networkx](https://networkx.org/) provides a [max_weight_matching](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.matching.max_weight_matching.html#max-weight-matching) ([max_weight_matching](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.matching.min_weight_matching.html#min-weight-matching) respectively) method that computes a maximum-weighted matching of a graph G. 

Currently the edge weights are defined in a way that guarantees that weights are positive:

$$
w_{ij} = K - (abs(age(P_i)-age(K_j)))^k
$$

