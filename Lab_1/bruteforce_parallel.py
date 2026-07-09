import random
import time
import threading
from itertools import combinations
import matplotlib.pyplot as plt

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

sizes = [5, 10, 15, 20, 25, 30]
activity_sets = {n: generate_activities(n) for n in sizes}

# -----------------------------
# Helper: check if a set of activities is mutually compatible
# -----------------------------
def is_compatible(subset):
    subset = sorted(subset, key=lambda x: x[1])
    for i in range(1, len(subset)):
        if subset[i][0] < subset[i - 1][1]:
            return False
    return True

# -----------------------------
# Brute Force Algorithm (single-threaded): try every subset (2^n),
# keep the largest compatible one
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
# Split-and-parallelize Brute Force:
# Divide the activities into two halves, brute-force each half
# independently in its own thread, then merge into one valid,
# mutually-compatible schedule.
# -----------------------------
def split_brute_force_activity_selection(activities):
    mid = len(activities) // 2
    half_a = activities[:mid]
    half_b = activities[mid:]

    half_results = {}
    lock = threading.Lock()

    def solve_half(label, acts):
        best = brute_force_activity_selection(acts)
        with lock:
            half_results[label] = best

    t1 = threading.Thread(target=solve_half, args=("A", half_a))
    t2 = threading.Thread(target=solve_half, args=("B", half_b))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    merged_candidates = list(half_results["A"]) + list(half_results["B"])
    merged_candidates.sort(key=lambda x: x[1])

    final_selection = []
    last_finish = float("-inf")
    for start, finish in merged_candidates:
        if start >= last_finish:
            final_selection.append((start, finish))
            last_finish = finish

    return final_selection

# -----------------------------
# Single-threaded brute force becomes impractical around n=30 (2^30 ~ 1 billion
# subsets, ~27 minutes based on the growth trend from smaller sizes). Skip
# running it past this size rather than blocking for that long.
# -----------------------------
SINGLE_THREADED_MAX_SIZE = 25

single_times = {}
split_times = {}
single_counts = {}
split_counts = {}

print("Brute Force: Single-threaded vs Split (Parallel) — Performance by Size")
print("-" * 75)

for n in sizes:
    activities = activity_sets[n]

    # Single-threaded brute force
    if n <= SINGLE_THREADED_MAX_SIZE:
        start = time.perf_counter()
        single_result = brute_force_activity_selection(activities)
        end = time.perf_counter()
        single_times[n] = end - start
        single_counts[n] = len(single_result)
        single_str = f"{single_times[n]:.6f}s (selected {single_counts[n]})"
    else:
        single_str = "skipped (impractical, ~2^30 subsets)"

    # Split (parallel) brute force
    start = time.perf_counter()
    split_result = split_brute_force_activity_selection(activities)
    end = time.perf_counter()
    split_times[n] = end - start
    split_counts[n] = len(split_result)

    print(f"n={n:2d} | Single-threaded: {single_str:38s} "
          f"| Split (parallel): {split_times[n]:.6f}s (selected {split_counts[n]})")

# -----------------------------
# Plot comparison
# -----------------------------
single_sizes = sorted(single_times.keys())
single_vals = [single_times[s] for s in single_sizes]

split_sizes = sorted(split_times.keys())
split_vals = [split_times[s] for s in split_sizes]

plt.figure(figsize=(8, 5))
plt.plot(single_sizes, single_vals, marker='o', linewidth=2, color='#c0392b',
         label='Single-threaded Brute Force')
plt.plot(split_sizes, split_vals, marker='o', linewidth=2, color='#8e44ad',
         label='Split Brute Force (parallel halves)')
plt.title("Brute Force: Single-threaded vs Split (Parallel) — Time vs Number of Activities")
plt.xlabel("Number of Activities (n)")
plt.ylabel("Time (seconds)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('./bruteforce_single_vs_split_plot.png', dpi=150)
print("\nPlot saved.")
print(f"\nNote: single-threaded brute force was skipped past n={SINGLE_THREADED_MAX_SIZE} "
      f"since it would take on the order of tens of minutes at n=30.")