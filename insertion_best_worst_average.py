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

def insertion_sort(arr):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

print("Insertion Sort Performance")
print("-" * 40)

sizes = []
avg_times = []
best_times = []
worst_times = []

for size, data in datasets.items():
    # Average case: random data (as given)
    arr_avg = data.copy()
    start = time.perf_counter()
    insertion_sort(arr_avg)
    avg_elapsed = time.perf_counter() - start

    # Best case: already sorted data
    arr_best = sorted(data)
    start = time.perf_counter()
    insertion_sort(arr_best)
    best_elapsed = time.perf_counter() - start

    # Worst case: reverse sorted data
    arr_worst = sorted(data, reverse=True)
    start = time.perf_counter()
    insertion_sort(arr_worst)
    worst_elapsed = time.perf_counter() - start

    sizes.append(size)
    avg_times.append(avg_elapsed)
    best_times.append(best_elapsed)
    worst_times.append(worst_elapsed)

    print(f"Input Size: {size:5d} | Avg: {avg_elapsed:.6f}s | "
          f"Best: {best_elapsed:.6f}s | Worst: {worst_elapsed:.6f}s")

# Plot
plt.figure(figsize=(8, 5))
plt.plot(sizes, avg_times, marker='o', linewidth=2, color='#2980b9', label='Average Case (Random)')
plt.plot(sizes, best_times, marker='s', linewidth=2, color='#27ae60', label='Best Case (Sorted)')
plt.plot(sizes, worst_times, marker='^', linewidth=2, color='#c0392b', label='Worst Case (Reverse Sorted)')
plt.title("Insertion Sort: Running Time vs Input Size")
plt.xlabel("Input Size (n)")
plt.ylabel("Time (seconds)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('./insertion_sort_best_worst_average_plot.png', dpi=150)
print("\nPlot saved.")