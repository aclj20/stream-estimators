import os
import time
import random
import tracemalloc
import pandas as pd
import matplotlib.pyplot as plt
from structures.sliding_window import SlidingWindowAggregator

os.makedirs("profiling_results", exist_ok=True)

NUM_POINTS = 10
STREAM_SIZES = [100 * (i + 1) for i in range(NUM_POINTS)]

csv_path = "profiling_results/profiling_sliding_window.csv"
with open(csv_path, "w") as f:
    f.write("stream_size,avg_insert_time_s,real_avg,estimated_avg,error_abs,error_rel,mem_usage_mb\n")
    for num_items in STREAM_SIZES:
        window_size = 50
        swa = SlidingWindowAggregator(window_size=window_size)
        data_stream = [random.randint(1, 1000) for _ in range(num_items)]

        real_window = data_stream[-window_size:]
        real_avg = sum(real_window) / len(real_window)

        tracemalloc.start()
        start = time.perf_counter()
        for item in data_stream:
            swa.update(item)
        elapsed = time.perf_counter() - start
        _, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        estimated_avg = swa.estimate()
        error_abs = abs(estimated_avg - real_avg)
        error_rel = error_abs / real_avg if real_avg != 0 else 0
        mem_usage_mb = peak_mem / (1024 ** 2)

        f.write(f"{num_items},{elapsed / num_items:.6e},{real_avg:.2f},{estimated_avg:.2f},{error_abs:.2f},{error_rel:.4f},{mem_usage_mb:.4f}\n")

print("Profiling Sliding Window completado y guardado.")

# Gráficas
df = pd.read_csv(csv_path)
plt.figure(figsize=(8, 4))
plt.plot(df["stream_size"], df["error_rel"], marker="o", label="Relative Error")
plt.xlabel("Stream Size")
plt.ylabel("Relative Error")
plt.title("Sliding Window: Relative Error")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("profiling_results/sliding_window_error.png", dpi=300)
