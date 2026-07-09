import random
import time
from itertools import combinations
import matplotlib.pyplot as plt
from activity_selection_greedy import greedy_activity_selection

random.seed(42)

# -----------------------------
# Generate random activities (start, finish) for a given n
# -----------------------------
def generate_activities(n):
    activities = []
    for _ in range(n):
        start = random.randint(0, 50)
        finish = start + random.randint(1, 15)
        activities.append((start, finish))
    return activities

sizes = [5, 10,15, 20,25]
activity_sets = {n: generate_activities(n) for n in sizes}

# -----------------------------
# Helper: check if a set of activities is mutually compatible
# -----------------------------
def is_compatible(subset):
    subset = sorted(subset, key=lambda x: x[1])  # sort by finish time
    for i in range(1, len(subset)):
        if subset[i][0] < subset[i - 1][1]:
            return False
    return True

# -----------------------------
# Brute Force Algorithm: try every subset (2^n), keep the largest compatible one
# -----------------------------
def brute_force_activity_selection(activities):
    n = len(activities)
    best = []
    for r in range(n, 0, -1):
        found = False
        for subset in combinations(activities, r):
            if is_compatible(subset):
                best = subset
                found = True
                break
        if found:
            break
    return best

# -----------------------------
# Time brute force algorithm across activity set sizes
# -----------------------------
brute_times = []

print("Activity Selection Problem Performance (Brute Force)")
print("-" * 60)

for n in sizes:
    activities = activity_sets[n]

    start = time.perf_counter()
    bf_result = brute_force_activity_selection(activities)
    end = time.perf_counter()
    bf_time = end - start
    brute_times.append(bf_time)

    print(f"n={n:2d} | Brute Force: {bf_time:.6f}s (selected {len(bf_result)})")

# -----------------------------
# Plot
# -----------------------------
plt.figure(figsize=(8, 5))
plt.plot(sizes, brute_times, marker='o', linewidth=2, color='#c0392b', label='Brute Force')
plt.title("Activity Selection (Brute Force): Running Time vs Number of Activities")
plt.xlabel("Number of Activities (n)")
plt.ylabel("Time (seconds)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('./activity_selection_bruteforce_plot.png', dpi=150)
print("\nPlot saved.")