import random

# Generate 30,000 random integers between 1 and 100,000
random.seed(42)  # Ensures the same numbers are generated every run
numbers = [random.randint(1, 100000) for _ in range(30000)]

# Create datasets of different sizes
data_1000 = numbers[:1000]
data_10000 = numbers[:10000]
data_20000 = numbers[:20000]
data_30000 = numbers[:30000]

# Verify sizes
print("1000 dataset size:", len(data_1000))
print("10000 dataset size:", len(data_10000))
print("20000 dataset size:", len(data_20000))
print("30000 dataset size:", len(data_30000))