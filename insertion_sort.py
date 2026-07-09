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
times = []
for size, data in datasets.items():
    arr = data.copy()
    start = time.perf_counter()
    insertion_sort(arr)
    end = time.perf_counter()
    elapsed = end - start
    sizes.append(size)
    times.append(elapsed)
    print(f"Input Size: {size:5d} | Time: {elapsed:.6f} seconds")
# Plot
plt.figure(figsize=(8, 5))
plt.plot(sizes, times, marker='o', linewidth=2, color='#2980b9')
plt.title("Insertion Sort: Running Time vs Input Size")
plt.xlabel("Input Size (n)")
plt.ylabel("Time (seconds)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('./insertion_sort_plot.png', dpi=150)
print("\nPlot saved.")