import os
import time
import random
import tracemalloc
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from structures.ams_sketch import AMSSketch

os.makedirs("profiling_results", exist_ok=True)

NUM_POINTS = 10
STREAM_SIZES = [100 * (i + 1) for i in range(NUM_POINTS)]

csv_path = "profiling_results/profiling_ams.csv"
with open(csv_path, "w") as f:
    f.write("stream_size,avg_insert_time_s,second_moment_real,second_moment_estimate,error_abs,error_rel,mem_usage_mb\n")
    for num_items in STREAM_SIZES:
        sketch = AMSSketch(num_projections=5)
        data_stream = [str(random.randint(1, 100)) for _ in range(num_items)]
        real_counts = Counter()

        tracemalloc.start()
        start = time.perf_counter()
        for item in data_stream:
            sketch.update(item)
            real_counts[item] += 1
        elapsed = time.perf_counter() - start
        _, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        second_moment_real = sum(freq**2 for freq in real_counts.values())
        estimate = sketch.estimate()
        error_abs = abs(estimate - second_moment_real)
        error_rel = error_abs / second_moment_real if second_moment_real != 0 else 0
        mem_usage_mb = peak_mem / (1024 ** 2)

        f.write(f"{num_items},{elapsed / num_items:.6e},{second_moment_real},{estimate:.2f},{error_abs:.2f},{error_rel:.4f},{mem_usage_mb:.4f}\n")

print("Profiling AMS completado y guardado.")

# Gráficas
df = pd.read_csv(csv_path)
plt.figure(figsize=(8, 4))
plt.plot(df["stream_size"], df["error_rel"], marker="o", label="Relative Error")
plt.xlabel("Stream Size")
plt.ylabel("Relative Error")
plt.title("AMS Sketch: Relative Error")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("profiling_results/ams_error.png", dpi=300)
