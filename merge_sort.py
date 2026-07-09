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

def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

print("Merge Sort Performance")
print("-" * 40)

sizes = []
times = []

for size, data in datasets.items():
    arr = data.copy()
    start = time.perf_counter()
    merge_sort(arr)
    end = time.perf_counter()
    elapsed = end - start
    sizes.append(size)
    times.append(elapsed)
    print(f"Input Size: {size:5d} | Time: {elapsed:.6f} seconds")

# Plot
plt.figure(figsize=(8, 5))
plt.plot(sizes, times, marker='o', linewidth=2, color='#2980b9')
plt.title("Merge Sort: Running Time vs Input Size")
plt.xlabel("Input Size (n)")
plt.ylabel("Time (seconds)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('./merge_sort_plot.png', dpi=150)
print("\nPlot saved.")