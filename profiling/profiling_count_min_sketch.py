import random
import time
import csv
import tracemalloc
from structures.count_min_sketch import CountMinSketch

EPSILON = 0.01
DELTA = 0.01
NUM_ITEMS_LIST = [10_000, 20_000, 30_000, 40_000, 50_000, 70_000, 100_000, 150_000, 200_000, 250_000, 300_000, 350_000, 400_000, 450_000, 500_000]
KEY_FIXED = "clave_fija"


def profile_frequency_error(output_csv):
    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["num_items", "real_count", "estimated_count", "abs_error", "rel_error", "mem_usage_MB"])
        
        for num_items in NUM_ITEMS_LIST:
            cms = CountMinSketch(epsilon=EPSILON, delta=DELTA)
            fixed_count = int(num_items*random.uniform(0.1, 0.9))

            data_stream = [KEY_FIXED] * fixed_count
            data_stream += [str(random.randint(1, 1_000_000)) for _ in range(num_items - len(data_stream))]
            random.shuffle(data_stream)

            tracemalloc.start()
            for item in data_stream:
                cms.update(item)
            _, peak_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            real_count = data_stream.count(KEY_FIXED)
            estimated_count = cms.estimate(KEY_FIXED)
            abs_error = abs(estimated_count - real_count)
            rel_error = abs_error / real_count if real_count != 0 else 0
            mem_usage_mb = peak_mem / (1024 ** 2)

            writer.writerow([num_items, real_count, estimated_count, abs_error, round(rel_error, 4), round(mem_usage_mb, 4)])

def profile_processing_speed(output_csv):
    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["num_items", "proc_speed_elems_per_sec"])
        
        for num_items in NUM_ITEMS_LIST:
            cms = CountMinSketch(epsilon=EPSILON, delta=DELTA)
            data_stream = [str(random.randint(1, 1_000_000)) for _ in range(num_items)]
            
            start_time = time.perf_counter()
            for item in data_stream:
                cms.update(item)
            end_time = time.perf_counter()

            proc_speed = num_items / (end_time - start_time)
            writer.writerow([num_items, round(proc_speed, 2)])

if __name__ == "__main__":
    profile_frequency_error("profiling_error_cms.csv")
    profile_processing_speed("profiling_speed_cms.csv")
