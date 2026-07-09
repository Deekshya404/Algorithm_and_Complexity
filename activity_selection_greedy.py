import random
import time
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

sizes = [5, 10, 20]
activity_sets = {n: generate_activities(n) for n in sizes}

# -----------------------------
# Greedy Algorithm: sort by finish time, then iteratively pick
# every activity whose start time is >= the finish time of the
# last selected activity
# -----------------------------
def greedy_activity_selection(activities):
    sorted_acts = sorted(activities, key=lambda x: x[1])  # sort by finish time
    selected = [sorted_acts[0]]
    last_finish = sorted_acts[0][1]

    for start, finish in sorted_acts[1:]:
        if start >= last_finish:
            selected.append((start, finish))
            last_finish = finish

    return selected

# -----------------------------
# Time greedy algorithm across activity set sizes
# -----------------------------
greedy_times = []

print("Activity Selection Problem Performance (Greedy)")
print("-" * 60)

for n in sizes:
    activities = activity_sets[n]

    start = time.perf_counter()
    greedy_result = greedy_activity_selection(activities)
    end = time.perf_counter()
    greedy_time = end - start
    greedy_times.append(greedy_time)

    print(f"n={n:2d} | Greedy: {greedy_time:.6f}s (selected {len(greedy_result)})")

# -----------------------------
# Plot
# -----------------------------
plt.figure(figsize=(8, 5))
plt.plot(sizes, greedy_times, marker='o', linewidth=2, color='#27ae60', label='Greedy')
plt.title("Activity Selection (Greedy): Running Time vs Number of Activities")
plt.xlabel("Number of Activities (n)")
plt.ylabel("Time (seconds)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('./activity_selection_greedy_plot.png', dpi=150)
print("\nPlot saved.")