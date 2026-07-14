"""
Fibonacci — Recursive (O(2^n)) vs Dynamic Programming / Tabulation (O(n))
=========================================================================
Single-file version: implementations + benchmarking + plotting.
"""

import sys
import time
import matplotlib.pyplot as plt

sys.setrecursionlimit(10000)


# ---------------------------------------------------------------------
# RECURSIVE — no memoization, re-solves the same subproblems repeatedly.
# T(n) = T(n-1) + T(n-2) + O(1)  =>  O(2^n)
# ---------------------------------------------------------------------
def fib_recursive(n):
    if n <= 1:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)


# ---------------------------------------------------------------------
# DYNAMIC PROGRAMMING (tabulation) — builds up a table from the bottom,
# each value computed exactly once. O(n) time, O(n) space.
# ---------------------------------------------------------------------
def fib_dp(n):
    if n <= 1:
        return n
    table = [0] * (n + 1)
    table[1] = 1
    for i in range(2, n + 1):
        table[i] = table[i - 1] + table[i - 2]
    return table[n]


def correctness_check():
    for n in range(10):
        assert fib_recursive(n) == fib_dp(n)
    print("fib_recursive and fib_dp agree for n=0..9")


def benchmark_and_plot():
    # Recursive: kept small (n=5..34) since it roughly doubles in time
    # for every +1 in n — anything past ~35 gets painfully slow.
    recursive_ns = list(range(5, 35))
    recursive_times = []
    for n in recursive_ns:
        t0 = time.perf_counter()
        fib_recursive(n)
        recursive_times.append(time.perf_counter() - t0)
        print(f"recursive n={n:2d}  time={recursive_times[-1]:.5f}s")

    # DP: same n range, PLUS a much larger range to show it stays fast.
    dp_ns = list(range(5, 35)) 
    dp_times = []
    for n in dp_ns:
        t0 = time.perf_counter()
        fib_dp(n)
        dp_times.append(time.perf_counter() - t0)
        print(f"dp n={n:5d}  time={dp_times[-1]:.7f}s")

    # Plot — both curves on the SAME graph, log-scale y-axis (the only
    # way an O(2^n) curve and an O(n) curve are readable together).
    plt.figure(figsize=(10, 6))
    plt.plot(recursive_ns, recursive_times, marker="o", color="#d62728",
              label="Recursive — O(2$^n$)")
    plt.plot(dp_ns, dp_times, marker="o", color="#1f77b4",
              label="DP / Tabulation — O(n)")
    plt.yscale("log")
    plt.xlabel("n (Fibonacci index)")
    plt.ylabel("Time (seconds, log scale)")
    plt.title("Fibonacci: Recursive O(2$^n$) vs DP Tabulation O(n)")
    plt.legend()
    plt.grid(True, which="both", alpha=0.3)
    plt.tight_layout()
    plt.savefig("fibonacci_comparison.png", dpi=150)
    print("Saved plot to fibonacci_comparison.png")


if __name__ == "__main__":
    correctness_check()
    benchmark_and_plot()