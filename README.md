# CI2024_lab3 - N-Puzzle Problem solution

![Solution Animation](docs/4x4.gif)

Implementing multiple algorithm to find a solution for the N-Puzzle problem

Description for N=15 : [`https://en.wikipedia.org/wiki/15_puzzle`](https://en.wikipedia.org/wiki/15_puzzle)

Since Keith Conrad proved that some configuration of the 15-Puzzle (and rubik's cube) cannot be solved: [`https://kconrad.math.uconn.edu/blurbs/grouptheory/15puzzle.pdf`](https://kconrad.math.uconn.edu/blurbs/grouptheory/15puzzle.pdf)

This algorithm start by creating the solution state and, making only legal moves to create the starting position, will create a starting state and only from that it will try to find the best moves to solve the problem.

If the algorithm didn't find any solution I miserably failed in the implementation :P


## Algorithm At work

Running the notebook this is the output you should expect:<br><br>

**Solution Grid** (4x4)

$$\begin{bmatrix}
  1  & 2  & 3  & 4       \\
  5  & 6  & 7  & 8       \\
  9  & 10 & 11 & 12      \\
  13 & 14 & 15 & \square
  \end{bmatrix}$$

**Starting State** (moves=20)

$$\begin{bmatrix}
  1  & 2  & 4       & 7  \\ 
  5  & 6  & 3       & 8  \\ 
  9  & 14 & \square & 11 \\ 
  13 & 15 & 10      & 12
\end{bmatrix}$$


| Dimension | Quality | Cost  |
| --------- | ------- | ----- |
| 4x4       | 13      | 34728 |



![Solution Animation](docs/4x4.gif)
(the output gif will actually be of the result with the correct number of steps)
## Data Analysis

### BFS

| Dimension | Quality | Cost  |
| --------- | ------- | ----- |
| 2x2       | 5       | 7     |
| 3x3       | 11      | 575   |
| 4x4       | 13      | 34728 |

> [!WARNING]
> As you can see the cost increase exponentially. <br>
> Keep in mind if you want to run $\ge 4$ dimensions to set a manual amount of moves (around 10 to 15).

### IDA Star

| Dimension | Quality | Cost   |
| --------- | ------- | ------ |
| 2x2       | 4       | 5      |
| 3x3       | 18      | 1025   |
| 4x4       | 38      | 13371  |
| 5x5       | 56      | 160867 |
| 15x15     | 50      | 1267   |

I wanted to try (even if with reduced complexity) the 15-problem. This show the actual dimension of the grid does not impact the algorithm as opposed to the BFS.

> [!NOTE]
> It may seems that the first 2x2 and 3x3 the IDA* performed better than the BFS
> until the 4x4, but really this problem size used a real random initial state instead, for the BFS, I had to reduce the number of legal starting steps to around 15  

When Reducing the problem complexity also for the  `IDA*` algorithm:
| Dimension | Quality | Cost |
| --------- | ------- | ---- |
| 4x4       | 13      | 19   |
| 4x4       | 28      | 2841 |

The cost for 13 (same number of steps of BFS) the cost is incredibly efficient and also 28 steps problem (more than double the BFS!), this new algorithm was $\approx12$ times more efficient!

## Installation
Using poetry just run `poetry install` and then the .venv will be created inside the project, after that using any tool you want, enable the new virtual environment to run the `n-puzzle.ipynb`

## Running the Solution

You are free to experiment and try different problem settings

In the notebook go to the latest cell and you will be greeted by:
* The dimension of the grid that you can choose:
  1. Use your custom number of moves: reduce the solution time (thus the initial entropy of the system) but the result are underwhelming as you can see below
     ![Example big problem with low entropy Solution Animation](docs/6x6.gif)
  2. Leave the formula (open the link and understand what it is doing) and make the (i hope) best random starting configuration
     ![Example big problem with low entropy Solution Animation](docs/3x3.gif)

Then you can choose:
1. one of the two kind of the same *Breadth-First Solver*
    * Linear: each new node is analyzed one after the another
      * `bfs_solver.solve(n_jobs=1)`: It's the default value, so really you can avoid passing any argument
    * Parallel: multiple node analyzed at the same time
      * `bfs_solver.solve(-1)` or set the actual number of of core you want to use
2. **Iterative deepening A***: That allow to find a solution using a variant of iterative deepening depth-first search using heuristic similar to the `A*` algorithm

> [!NOTE]
> In my testing the Parallel performed worse.<br>
> Maybe the overhead to instantiate multiple jobs was too much with respect of the amount of node to analyze simultaneously
> Still I think it was worth trying and thus leaved there so that You can playing around if you like

Then you have to pass the starting and goal grid to create to your selected solver

If you want you can try to run the algorithm yourself with a low entropy to have an immediate, flashing, gifs in front of you that show how your random problem can be solved!

This is done both to make a pretty solution and to make the reviewer understand that those gifs around this document weren't personally made (I am terrible at this puzzle!) but procedurally created based on the solution of given by the algorithm

One last thing:

**Have fun!** :D