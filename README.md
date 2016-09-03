## Title
Analysis of Greedy Algorithm Framework for Choosing Network-Probing Paths
Colgate University (Summer Research 2016)

Poster Link: https://drive.google.com/a/colgate.edu/file/d/0BxUOgM_nH9qCZjkxS3UyRTVHR3c/view?usp=sharing

## Synopsis

The project is to implement a greedy heuristic for probing-path selection that can simultaneously consider multiple overhead- minimization objectives.

## Motivation

Research Motivation:

- Many existing approaches to probing-path selection seek to minimize the number of probes (an NP-hard problem) or 
to minimize probing delay, but they fail to properly assess the network overhead imposed by the probing strategy.

- We present a general greedy heuristic for probing-path selection that can simultaneously consider multiple overhead- minimization objectives.

Codebase Motivation:

- We have developed this codebase to support our greedy framework to investigate tradeoffs among different optimization goals,
- To ease the process of analyzing data, we have also developed scripts that automatically creates scatter plots from our data

## Installation

Download all the script files, and type the following to run from the terminal:

(for MacOS, Linux)

```shell
python summer_research_main.py filename1.txt filename2.txt
```
where
filename1.txt - contains the graph parameters in the form: 
(0 50 0.23 4 1 10 9)

(graph_id number_of_nodes edge_probability graph_seed lowest_edge_weight highest_edge_weight random_seed)

filename2.txt - contains the coefficient or fraction in the form:
0.1