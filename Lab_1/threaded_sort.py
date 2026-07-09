import random
import time
import threading
import matplotlib.pyplot as plt

random.seed(42)
numbers = [random.randint(1, 100000) for _ in range(30000)]

datasets = {
    1000: numbers[:1000],
    10000: numbers[:10000],
    20000: numbers[:20000],
    30000: numbers[:30000]
}

def selection_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        min_index = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]

# results dict shared across threads, guarded by a lock
results = {}
lock = threading.Lock()

def timed_sort(size, data):
    arr = data.copy()
    start = time.perf_counter()
    selection_sort(arr)
    end = time.perf_counter()
    elapsed = end - start
    with lock:
        results[size] = elapsed
    print(f"Input Size: {size:5d} | Time: {elapsed:.6f} seconds")

# One thread per dataset size
threads = []
for size, data in datasets.items():
    t = threading.Thread(target=timed_sort, args=(size, data))
    threads.append(t)

print("Selection Sort Performance (each size on its own thread)")
print("-" * 60)

overall_start = time.perf_counter()

for t in threads:
    t.start()

for t in threads:
    t.join()

overall_end = time.perf_counter()
print("-" * 60)
print(f"All threads finished. Wall-clock time: {overall_end - overall_start:.6f} seconds")

sizes = sorted(results.keys())
times = [results[s] for s in sizes]

plt.figure(figsize=(8, 5))
plt.plot(sizes, times, marker='o', linewidth=2, color='#d35400')
plt.title("Selection Sort (Each Size on Its Own Thread): Time vs Input Size")
plt.xlabel("Input Size (n)")
plt.ylabel("Time (seconds)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('./threaded_by_size_plot.png', dpi=150)
print("\nPlot saved.")