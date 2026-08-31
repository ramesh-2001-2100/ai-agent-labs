import numpy as np
import time

# Find all numbers > 50 in a million-element array
start = time.time()
data = np.random.randint(0, 100, 1_000_000)
filtered = data[data > 50]  # One line, C-speed
end = time.time()
print("elapsed time for the numpy operation:", end - start)
