import random
import time
import matplotlib.pyplot as plt

random.seed(42)
numbers = [random.randint(1, 100000) for _ in range(30000)]

datasets = {
    1000: numbers[:2000],
    4000: numbers[:4000],
    6000: numbers[:6000],
    8000: numbers[:8000]
}

def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)

print("Heap Sort Performance")
print("-" * 40)

sizes = []
times = []

for size, data in datasets.items():
    arr = data.copy()
    start = time.perf_counter()
    heap_sort(arr)
    end = time.perf_counter()
    elapsed = end - start
    sizes.append(size)
    times.append(elapsed)
    print(f"Input Size: {size:5d} | Time: {elapsed:.6f} seconds")

# Plot
plt.figure(figsize=(8, 5))
plt.plot(sizes, times, marker='o', linewidth=2, color='#8e44ad')
plt.title("Heap Sort: Running Time vs Input Size")
plt.xlabel("Input Size (n)")
plt.ylabel("Time (seconds)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('./heap_sort_plot.png', dpi=150)
print("\nPlot saved.")