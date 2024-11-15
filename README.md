# CI2024_lab3 - N-Puzzle Problem solution

![Solution Animation](docs/4x4.gif)

Implementing multiple algorithm to find a solution for the N-Puzzle problem

Description for N=15 : [`https://en.wikipedia.org/wiki/15_puzzle`](https://en.wikipedia.org/wiki/15_puzzle)

Since Keith Conrad proved that some configuration of the 15-Puzzle (and rubik's cube) cannot be solved: [`https://kconrad.math.uconn.edu/blurbs/grouptheory/15puzzle.pdf`](https://kconrad.math.uconn.edu/blurbs/grouptheory/15puzzle.pdf)

This algorithm start by creating the solution state and, making only legal moves to create the starting position, will create a starting state and only from that it will try to find the best moves to solve the problem.

If the algorithm didn't find any solution I miserably failed in the implementation :P


## Algorithm At work

Running the notebook this is the output you should expect:
```ps
Starting Grid:
[[ 6  5  2  3]
 [ 9  1 11  4]
 [ 7 15  0  8]
 [13 10 14 12]]

Solution Grid:
[[ 1  2  3  4]
 [ 5  6  7  8]
 [ 9 10 11 12]
 [13 14 15  0]]
-------------------
BFS: Solved in 20 number of steps
```

![Solution Animation](docs/4x4.gif)


## Installation
Using poetry just run `poetry install` and then the .venv will be created inside the project, after that using any tool you want, enable the new virtual environment to run the `n-puzzle.ipynb`

## Running the Solution

You are free to experiment and try different problem settings

In the notebook go to the latest cell and you will be greeted by:

```python
dim = 4
moves = 20

# Generate a NxN solution grid in order from 0 to 15
goal_state: NDArray[np.int32] = generate_goal_state(dim)

# Generate a NxN grid of random numbers from 0 to 15
initial_state: NDArray[np.int32] = scramble_state(goal_state, moves)

print("Starting Grid:")
print(initial_state)
print()
print("Solution Grid:")
print(goal_state)
print("-------------------")

# Solve using Breadth First Search
bfs_path = BFS(initial_state, goal_state).solve()
if bfs_path:
    save_solution_gif(bfs_path)
```

Although It seems a lot, the first two lines let you setup the dimension of the grid and the number of random legal moves to make before starting solving the problem.

If you want you can modify the name of the output gif to be sure I didn't cheat with a prerecorder solution :P

Have fun!