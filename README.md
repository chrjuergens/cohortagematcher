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

The package [networkx](https://networkx.org/) provides a [max_weight_matching](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.matching.max_weight_matching.html#max-weight-matching) ([min_weight_matching](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.matching.min_weight_matching.html#min-weight-matching) respectively) method that computes a maximum-weighted matching (minimum-weighted matchin respectively) of a graph G.

Currently the age difference is defined as the absolute value of the difference of the ages of $P_i$ and $K_j$:

$$
d_{ij} = abs(age(P_i)-age(K_j))
$$


In case of **minimum-weighted matching** one can use the weights

$$
w_{ij} = d_{ij}^s
$$

where $s$ is an integer.
With $s>1$ edges with bigger $d_{ij}$ get a bigger weight $w_{ij}$ assigned.
The minimum-weighted matching algorithm will try to avoid these edges.
Hence, $s>1$ can be seen as outlier prevention as the weights of all edges in the resulting matching will have comparable weights.

