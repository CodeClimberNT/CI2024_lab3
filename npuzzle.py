from collections import deque
import sys
import os

from typing import Any, Deque

import numpy as np
from numpy.typing import NDArray

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import artist
import imageio.v2 as imageio

# Increase recursion limit for DFS and IDS
sys.setrecursionlimit(10000)

# Default initial and goal states
DEFAULT_INITIAL_STATE: NDArray = np.array(
    [
        [1, 2, 3],
        [4, 5, 6],
        [0, 7, 8],
    ]
)

DEFAULT_GOAL_STATE: NDArray = np.array(
    [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0],
    ]
)


def visualize_solution(path, output_dir='puzzle_solutions', gif_name='solution.gif', fps=1):
    """
    Saves a GIF of the N-puzzle solution path using matplotlib.animation.

    Args:
        path (list of np.ndarray or list): List of puzzle states representing the solution path.
            Each state should be a 2D NumPy array of shape (N, N) with values from 0 to N^2-1.
        output_dir (str): Directory to save the GIF. Defaults to 'puzzle_solutions'.
        gif_name (str): Name of the output GIF file. Defaults to 'solution.gif'.
        fps (int): Frames per second for the GIF. Defaults to 1.
    """
    if not path:
        print("No solution path provided")
        return

    os.makedirs(output_dir, exist_ok=True)

    # Determine the size of the puzzle
    first_state = path[0]
    if isinstance(first_state, list):
        first_state = np.array(first_state)
    if not isinstance(first_state, np.ndarray):
        print("Invalid state type. Each state must be a NumPy array or a list.")
        return
    if first_state.ndim == 1 and first_state.size == first_state.shape[0] ** 2:
        N = int(np.sqrt(first_state.size))
    elif first_state.ndim == 2 and first_state.shape[0] == first_state.shape[1]:
        N = first_state.shape[0]
    else:
        print(f"Invalid state shape: {first_state.shape}. Each state must be a square 2D array.")
        return

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.axis('off')

    frames = []

    for i, state in enumerate(path):
        # Convert state to NumPy array if it's a list
        if isinstance(state, list):
            state = np.array(state)

        # Reshape state if it's a 1D array
        if state.ndim == 1 and state.size == N * N:
            state = state.reshape(N, N)
        elif state.ndim != 2 or state.shape != (N, N):
            print(f"Invalid state at step {i}: shape {state.shape}. Skipping this state.")
            continue

        # Clear previous texts and images
        ax.clear()
        ax.axis('off')

        # Display the board as a table
        table = ax.table(cellText=state.tolist(), loc='center', cellLoc='center')
        table.scale(1, 1.5)  # Adjust table size as needed

        # Style the table
        for (row, col), cell in table.get_celld().items():
            if state[row, col] == 0:
                cell.set_facecolor('#FFFFFF')  # White for empty tile
            else:
                # You can customize colors based on the tile number if desired
                cell.set_facecolor('#ADD8E6')  # Light blue for numbered tiles
            cell.set_edgecolor('black')

        # Add title indicating the step number
        ax.set_title(f'Step {i}', fontsize=16)

        # Append the artists to frames
        frames.append([table])

    if frames:
        # Create the animation using ArtistAnimation
        ani = animation.ArtistAnimation(fig, frames, interval=1000 / fps, blit=True, repeat=False)

        # Save the animation as a GIF
        gif_path = os.path.join(output_dir, gif_name)
        ani.save(gif_path, writer='pillow')
        plt.close(fig)
        print(f"Solution GIF saved at {gif_path}")
    else:
        print("No valid frames to save as GIF.")


def get_neighbors(state) -> NDArray:
    neighbors: list[int] = []
    x, y = np.argwhere(state == 0)[0]
    moves: list[tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < state.shape[0] and 0 <= ny < state.shape[1]:
            new_state = state.copy()
            new_state[x, y], new_state[nx, ny] = new_state[nx, ny], new_state[x, y]
            neighbors.append(new_state)
    return np.array(neighbors)


def search_util(current_state, goal_state, visited, path, depth, max_depth):
    if depth > max_depth:
        return None
    if np.array_equal(current_state, goal_state):
        return path + [current_state]
    visited.add(current_state.tostring())
    for neighbor in get_neighbors(current_state):
        if neighbor not in visited:
            result = search_util(neighbor, goal_state, visited, path + [current_state], depth + 1, max_depth)
            if result is not None:
                return result
    return None


class BFS:
    def __init__(self, initial_state=DEFAULT_INITIAL_STATE, goal_state=DEFAULT_GOAL_STATE) -> None:
        self.initial_state: NDArray = initial_state
        self.goal_state: NDArray = goal_state
        # The initial state is the first visited state
        self.visited: list[bytes] = [initial_state.tobytes()]
        self.queue: Deque[tuple[NDArray, list]] = deque()

    def solve(self) -> list | None:
        self.queue.append((self.initial_state, []))

        while self.queue:
            current_state, path = self.queue.popleft()
            if np.array_equal(current_state, self.goal_state):
                print(f"BFS: Number of steps = {len(path)}")
                return path + current_state.tolist()
            for neighbor in get_neighbors(current_state):
                if neighbor.tobytes() not in self.visited:
                    self.visited.append(neighbor.tobytes())
                    self.queue.append((neighbor, path + [current_state]))
        print("BFS: No solution found")
        _, path = self.queue.pop()
        print(f"Tried Path = {path}")
        return None


class DFS:
    def __init__(self, initial_state=DEFAULT_INITIAL_STATE, goal_state=DEFAULT_GOAL_STATE) -> None:
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.visited = set()
        self.path = []
        self.depth = 0
        self.max_depth = sys.getrecursionlimit()

    def solve(self):
        self.path = search_util(self.initial_state, self.goal_state, self.visited, [], self.depth, self.max_depth)
        if self.path is not None:
            print(f"DFS: Number of steps = {len(self.path) - 1}")
            return self.path
        else:
            print("DFS: No solution found")
            return None


class IDS:
    def __init__(self, initial_state=DEFAULT_INITIAL_STATE, goal_state=DEFAULT_GOAL_STATE):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.visited = set()
        self.path = []
        self.max_depth = 0

    def solve(self):
        while True:
            self.visited = set()
            self.path = search_util(self.initial_state, self.goal_state, self.visited, [], 0, self.max_depth)
            if self.path is not None:
                print(f"IDS: Number of steps = {len(self.path) - 1}")
                return self.path
            self.max_depth += 1
        print("IDS: No solution found")
        print("Anyway: How did you get here?")
        return None


def main():
    initial_state = DEFAULT_INITIAL_STATE
    goal_state = DEFAULT_GOAL_STATE

    # Solve using Breadth First Search
    bfs_path = BFS(initial_state, goal_state).solve()
    if bfs_path:
        visualize_solution(bfs_path)

    # # Solve using Deep First Search
    # dfs_path = DFS(initial_state, goal_state).solve()
    # if dfs_path:
    #     visualize_solution(dfs_path)

    # # Solve using Iterative Deepening Search
    # ids_path = IDS(initial_state, goal_state).solve()
    # if ids_path:
    #     visualize_solution(ids_path)


if __name__ == "__main__":
    main()
