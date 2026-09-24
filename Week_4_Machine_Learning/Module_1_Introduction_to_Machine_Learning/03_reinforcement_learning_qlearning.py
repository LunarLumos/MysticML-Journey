"""
03_reinforcement_learning_qlearning.py
======================================
Week 4 · Module 1 – Machine Learning Types → REINFORCEMENT LEARNING

Reinforcement learning (RL) = an AGENT learns by trial and error inside an
ENVIRONMENT. There are no labels – only REWARDS after each ACTION.

This script trains a tabular Q-learning agent (pure NumPy) on a 4×4 gridworld:

    S . . .        S = start (0,0)
    . # . #        # = hole (reward -1, episode ends)
    . . . #        G = goal (reward +1, episode ends)
    # . . G        every normal step costs -0.01 (encourages short paths)

Q-learning update rule (Bellman):
    Q(s,a) ← Q(s,a) + α · [ r + γ · max_a' Q(s',a') − Q(s,a) ]

Run:
    python 03_reinforcement_learning_qlearning.py [--episodes 2000]
"""

import argparse

import numpy as np

GRID = [
    "S...",
    ".#.#",
    "...#",
    "#..G",
]
ACTIONS = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1)}  # up, down, left, right
ARROWS = {0: "↑", 1: "↓", 2: "←", 3: "→"}
N_ROWS, N_COLS = len(GRID), len(GRID[0])


# ---------------------------------------------------------------
# The ENVIRONMENT
# ---------------------------------------------------------------
def step(state: int, action: int) -> tuple[int, float, bool]:
    """Apply an action; return (next_state, reward, episode_done)."""
    row, col = divmod(state, N_COLS)
    d_row, d_col = ACTIONS[action]
    # Walls: bumping into the edge keeps the agent in place.
    row = min(max(row + d_row, 0), N_ROWS - 1)
    col = min(max(col + d_col, 0), N_COLS - 1)
    cell = GRID[row][col]
    next_state = row * N_COLS + col
    if cell == "G":
        return next_state, 1.0, True
    if cell == "#":
        return next_state, -1.0, True
    return next_state, -0.01, False


# ---------------------------------------------------------------
# The AGENT (Q-learning)
# ---------------------------------------------------------------
def train_q_learning(episodes: int = 2000, alpha: float = 0.1, gamma: float = 0.95,
                     epsilon: float = 1.0, seed: int = 42) -> np.ndarray:
    """Train a Q-table with epsilon-greedy exploration and return it."""
    rng = np.random.default_rng(seed)
    q_table = np.zeros((N_ROWS * N_COLS, len(ACTIONS)))
    successes = 0
    for episode in range(1, episodes + 1):
        state, done, steps = 0, False, 0
        while not done and steps < 100:
            # Explore (random action) or exploit (best known action)?
            if rng.random() < epsilon:
                action = int(rng.integers(len(ACTIONS)))
            else:
                action = int(np.argmax(q_table[state]))
            next_state, reward, done = step(state, action)
            # Bellman update: move Q towards reward + discounted future value.
            target = reward + (0 if done else gamma * np.max(q_table[next_state]))
            q_table[state, action] += alpha * (target - q_table[state, action])
            state, steps = next_state, steps + 1
            if done and reward > 0:
                successes += 1
        epsilon = max(0.05, epsilon * 0.995)  # explore less over time
        if episode % (episodes // 4) == 0:
            print(f"[+] Episode {episode:5d} | epsilon={epsilon:.3f} | "
                  f"goals reached so far: {successes}")
    return q_table


def show_policy(q_table: np.ndarray) -> None:
    """Print the greedy policy (best action per cell) as arrows."""
    print("\n[*] Learned policy (best action in each cell):")
    for row in range(N_ROWS):
        line = ""
        for col in range(N_COLS):
            cell = GRID[row][col]
            if cell in "#G":
                line += f" {cell} "
            else:
                line += f" {ARROWS[int(np.argmax(q_table[row * N_COLS + col]))]} "
        print("    " + line)


def run_greedy_episode(q_table: np.ndarray) -> list[tuple[int, int]]:
    """Follow the learned policy from the start and return the path."""
    state, done, path = 0, False, [(0, 0)]
    while not done and len(path) < 20:
        state, reward, done = step(state, int(np.argmax(q_table[state])))
        path.append(divmod(state, N_COLS))
    return path


def main() -> None:
    """Train the agent, show its policy and one greedy run."""
    parser = argparse.ArgumentParser(description="Q-learning on a tiny gridworld")
    parser.add_argument("--episodes", type=int, default=2000)
    args = parser.parse_args()

    print("=" * 60)
    print("Reinforcement Learning · Q-learning on a 4x4 gridworld")
    print("=" * 60)
    q_table = train_q_learning(episodes=args.episodes)
    show_policy(q_table)
    path = run_greedy_episode(q_table)
    reached = GRID[path[-1][0]][path[-1][1]] == "G"
    print(f"\n[*] Greedy path from S: {path}")
    print(f"[*] Reached the goal: {reached}  (in {len(path) - 1} steps)")


if __name__ == "__main__":
    main()
