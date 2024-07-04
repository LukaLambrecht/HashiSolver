# Solver for Hashi puzzles

### Prerequisites
Required:
- `python` (developed in 3.8, not sure about other versions)
- `numpy`

Optional:
- `bokeh` (for the graphical interface)

### Preparing the input
You'll need your Hashi puzzle to solve in the form of a `.txt` file.
Use a single digit (the number of connection to make) for each vertex, and a dash (`-`) for positions without a vertex.
Consider the following example:

The corresponing `.txt` file would look like this:

```
4-4---2
---2---
3---1-3
---4-1-
-------
1--2--2
--2--1-
```

### Running the solver
Use `python solve.py <path to input file>`.
Using the example from above, the terminal output will look like this:

```
---------------
|4   4       2|
|             |
|      2      |
|             |
|3       1   3|
|             |
|      4   1  |
|             |
|             |
|             |
|1     2     2|
|             |
|    2     1  |
---------------
---------------
|4===4-------2|
|"   |       ||
|"   | 2     ||
|"   | "     ||
|3   | " 1---3|
||   | "     ||
||   | 4---1 ||
||   | |     ||
||   | |     ||
||   | |     ||
|1   | 2-----2|
|    |        |
|    2-----1  |
---------------
Complete: True
```
