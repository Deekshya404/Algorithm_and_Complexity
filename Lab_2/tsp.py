"""
Travelling Salesman Problem — Bus Driver Route
================================================
A bus driver starts at the school (node 0) and must drop off kids at
their 9 homes (nodes 1..9), visiting each exactly once. We want the
shortest total distance/time.

  - Brute force : tries every possible visiting order. Exact optimal,
                  but O((n-1)!) since the start node is fixed.
  - Greedy      : nearest-neighbor heuristic — from the current stop,
                  always go to the closest home not yet visited.
                  O(n^2), fast, but not guaranteed optimal.

Single-file version: implementations + demo + benchmarking + plotting.
"""

import itertools
import random
import time
import sys
import matplotlib.pyplot as plt

sys.setrecursionlimit(10000)


# ---------------------------------------------------------------------
# Random distance/time matrix between school + kids' homes
# ---------------------------------------------------------------------
def generate_distance_matrix(n_locations, seed=None):
    """
    n_locations includes the school (index 0) plus each kid's home.
    Returns a symmetric matrix of random travel times (minutes).
    """
    rnd = random.Random(seed)
    matrix = [[0] * n_locations for _ in range(n_locations)]
    for i in range(n_locations):
        for j in range(i + 1, n_locations):
            t = rnd.randint(2, 30)  # minutes between two locations
            matrix[i][j] = t
            matrix[j][i] = t
    return matrix


def route_cost(route, dist):
    """Total travel time for a route (list of node indices, in order)."""
    return sum(dist[route[i]][route[i + 1]] for i in range(len(route) - 1))


# ---------------------------------------------------------------------
# BRUTE FORCE — try every permutation of the drop-off order.
# Start (school, node 0) is fixed, so we only permute the other n-1
# nodes => (n-1)! orderings instead of n!.
# ---------------------------------------------------------------------
def tsp_brute_force(dist, start=0):
    n = len(dist)
    other_nodes = [i for i in range(n) if i != start]

    best_route = None
    best_cost = float("inf")

    for perm in itertools.permutations(other_nodes):
        route = [start] + list(perm)
        cost = route_cost(route, dist)
        if cost < best_cost:
            best_cost = cost
            best_route = route

    return best_route, best_cost


# ---------------------------------------------------------------------
# GREEDY (nearest neighbor) — from the current stop, always go to the
# nearest home not yet visited. Fast, but can miss the true optimum.
# ---------------------------------------------------------------------
def tsp_greedy(dist, start=0):
    n = len(dist)
    visited = [start]
    unvisited = set(range(n)) - {start}

    while unvisited:
        current = visited[-1]
        nearest = min(unvisited, key=lambda node: dist[current][node])
        visited.append(nearest)
        unvisited.remove(nearest)

    return visited, route_cost(visited, dist)


# ---------------------------------------------------------------------
# Demo: 10 locations = 1 school + 9 kids' homes (bus starts at school)
# ---------------------------------------------------------------------
def run_demo():
    n_locations = 10
    dist = generate_distance_matrix(n_locations, seed=42)
    names = ["School"] + [f"Home_{i}" for i in range(1, n_locations)]

    brute_route, brute_cost = tsp_brute_force(dist)
    greedy_route, greedy_cost = tsp_greedy(dist)

    print("Brute force route:", [names[i] for i in brute_route])
    print("Brute force total time:", brute_cost, "minutes")
    print()
    print("Greedy route:      ", [names[i] for i in greedy_route])
    print("Greedy total time:      ", greedy_cost, "minutes")


# ---------------------------------------------------------------------
# Benchmark + plot: brute force vs greedy time complexity
# ---------------------------------------------------------------------
def benchmark_and_plot():
    # 1) Small n: brute force vs greedy, head to head.
    #    Brute force is (n-1)! — already ~0.4s at n=10, so we stop there.
    small_ns = list(range(3, 11))  # 3..10 locations
    brute_times = []
    greedy_times_small = []

    for n in small_ns:
        dist = generate_distance_matrix(n, seed=1)

        t0 = time.perf_counter()
        tsp_brute_force(dist)
        brute_times.append(time.perf_counter() - t0)

        t0 = time.perf_counter()
        tsp_greedy(dist)
        greedy_times_small.append(time.perf_counter() - t0)

        print(f"n={n:2d}  brute={brute_times[-1]:.5f}s  greedy={greedy_times_small[-1]:.7f}s")

    # 2) Large n: greedy only, to show it stays fast (O(n^2)) far beyond
    #    where brute force becomes impossible.
    large_ns = [10, 20, 50, 100, 200, 400, 700, 1000]
    greedy_times_large = []

    for n in large_ns:
        dist = generate_distance_matrix(n, seed=7)
        t0 = time.perf_counter()
        tsp_greedy(dist)
        greedy_times_large.append(time.perf_counter() - t0)
        print(f"n={n:5d}  greedy={greedy_times_large[-1]:.5f}s")

    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))

    # Left: brute force vs greedy, log-scale y axis
    ax = axes[0]
    ax.plot(small_ns, brute_times, marker="o", color="#d62728",
            label="Brute force — O((n-1)!)")
    ax.plot(small_ns, greedy_times_small, marker="o", color="#1f77b4",
            label="Greedy (nearest neighbor) — O(n$^2$)")
    ax.set_yscale("log")
    ax.set_xlabel("Number of locations (school + homes)")
    ax.set_ylabel("Time (seconds, log scale)")
    ax.set_title("Bus Route TSP: Brute Force vs Greedy\n(small n, note the log scale)")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)

    # Right: greedy alone, larger n, to show its O(n^2) scaling
    ax = axes[1]
    ax.plot(large_ns, greedy_times_large, marker="o", color="#1f77b4")
    ax.set_xlabel("Number of locations")
    ax.set_ylabel("Time (seconds)")
    ax.set_title("Greedy Nearest-Neighbor Scaling\n(large n, ~O(n$^2$))")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.figtext(0.9, 0.01, "Prepared by: Deekshya Badal",
            ha="center", fontsize=10)
    plt.savefig("tsp_comparison.png", dpi=150)
    print("Saved plot to tsp_comparison.png")


if __name__ == "__main__":
    run_demo()
    print()
    benchmark_and_plot()