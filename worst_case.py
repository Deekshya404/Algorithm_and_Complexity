from heap_sort import heap_sort
from insertion_sort import insertion_sort
from merge_sort import merge_sort
from quick_sort import quick_sort
from selection_sort import selection_sort
import random
import time
import matplotlib.pyplot as plt

random.seed(42)
numbers = [random.randint(1, 100000) for _ in range(30000)]

datasets = {
    2000: numbers[:2000],
    4000: numbers[:4000],
    6000: numbers[:6000],
    8000: numbers[:8000]
}
sizes = list(datasets.keys())

# merge_sort and quick_sort return a new list instead of sorting in place,
# so wrap them to match the in-place signature of the others
def run_merge_sort(arr):
    arr[:] = merge_sort(arr)

def run_quick_sort(arr):
    arr[:] = quick_sort(arr)

algorithms = {
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": run_merge_sort,
    "Quick Sort": run_quick_sort,
    "Heap Sort": heap_sort,
}

colors = {
    "Selection Sort": "#d35400",
    "Insertion Sort": "#2980b9",
    "Merge Sort": "#27ae60",
    "Quick Sort": "#8e44ad",
    "Heap Sort": "#c0392b",
}

# Candidate input patterns to test — the true worst case for each
# algorithm depends on its pivot/comparison strategy, so we try
# several orderings and keep whichever is actually slowest.
def get_patterns(data):
    return {
        "Ascending": sorted(data),
        "Descending": sorted(data, reverse=True),
    }

results = {name: [] for name in algorithms}
worst_pattern_used = {name: [] for name in algorithms}

print("Empirical Worst Case Performance (slowest of tested patterns)")
print("-" * 60)

for name, func in algorithms.items():
    print(f"\n{name}")
    for size, data in datasets.items():
        patterns = get_patterns(data)
        slowest_time = -1
        slowest_pattern = None

        for pattern_name, pattern_data in patterns.items():
            arr = pattern_data.copy()
            start = time.perf_counter()
            func(arr)
            elapsed = time.perf_counter() - start

            if elapsed > slowest_time:
                slowest_time = elapsed
                slowest_pattern = pattern_name

        results[name].append(slowest_time)
        worst_pattern_used[name].append(slowest_pattern)
        print(f"Input Size: {size:5d} | Worst: {slowest_time:.6f}s | Pattern: {slowest_pattern}")

# Plot
plt.figure(figsize=(9, 6))
for name, times in results.items():
    plt.plot(sizes, times, marker='o', linewidth=2, label=name, color=colors[name])

plt.title("Sorting Algorithms: True Worst Case Running Time vs Input Size")
plt.xlabel("Input Size (n)")
plt.ylabel("Time (seconds)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('./all_sorts_true_worst_case_plot.png', dpi=150)
print("\nPlot saved.")

print("\nWorst-case pattern per algorithm per size:")
for name, patterns in worst_pattern_used.items():
    print(f"{name}: {patterns}")