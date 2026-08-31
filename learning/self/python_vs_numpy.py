import time
import numpy as np

# Python list of 10 million numbers
numbers = list(range(10_000_000))

start = time.time()
total = 0
for num in numbers:
    total += num
end = time.time()

print(f"Python loop: {end - start:.4f} seconds")
# Output: ~0.65 seconds (on my machine)


# NumPy array of 10 million numbers
numbers_np = np.arange(10_000_000)

start = time.time()
total = numbers_np.sum()  # This runs in C!
end = time.time()

print(f"NumPy loop: {end - start:.4f} seconds")
# Output: ~0.0058 seconds — that's 112x times faster!