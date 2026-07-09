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

case_colors = {
    "Best (Sorted)": "#27ae60",
    "Average (Random)": "#2980b9",
    "Worst (Reverse Sorted)": "#c0392b",
}

# results[algo_name][case_name] = list of times, one per size
results = {name: {case: [] for case in case_colors} for name in algorithms}

for name, func in algorithms.items():
    print(f"\n{name} Performance")
    print("-" * 40)
    for size, data in datasets.items():
        cases = {
            "Best (Sorted)": sorted(data),
            "Average (Random)": data,
            "Worst (Reverse Sorted)": sorted(data, reverse=True),
        }
        for case_name, case_data in cases.items():
            arr = case_data.copy()
            start = time.perf_counter()
            func(arr)
            end = time.perf_counter()
            elapsed = end - start
            results[name][case_name].append(elapsed)
            print(f"Input Size: {size:5d} | {case_name:24s} | Time: {elapsed:.6f} seconds")

# Plot: grid of subplots, one per algorithm
fig, axes = plt.subplots(2, 3, figsize=(16, 9))
axes = axes.flatten()

for idx, (name, cases) in enumerate(results.items()):
    ax = axes[idx]
    for case_name, times in cases.items():
        ax.plot(sizes, times, marker='o', linewidth=2, label=case_name, color=case_colors[case_name])
    ax.set_title(name)
    ax.set_xlabel("Input Size (n)")
    ax.set_ylabel("Time (seconds)")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)

# Hide the unused 6th subplot slot
axes[-1].axis('off')

plt.suptitle("Sorting Algorithms: Best / Average / Worst Case Running Time", fontsize=14)
plt.tight_layout()
plt.savefig('./all_sorts_best_avg_worst_plot.png', dpi=150)
print("\nPlot saved.")