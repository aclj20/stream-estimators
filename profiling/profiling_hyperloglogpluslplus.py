import time, random, tracemalloc, csv, os
from structures.hyperloglogpp import HyperLogLogPlusPlus

OUTPUT_DIR = "profiling_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)
CSV_FILE = os.path.join(OUTPUT_DIR, "hyperloglog_profile.csv")

with open(CSV_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["num_elements", "avg_update_time_us",  "true_cardinality", "est_cardinality","abs_error", "rel_error", "mem_usage_mb"])

    NUM_ELEMENTS_LIST = [10_000, 20_000, 30_000, 40_000, 50_000, 70_000, 100_000, 150_000, 200_000, 250_000, 300_000, 350_000, 400_000, 450_000, 500_000]

    for n in NUM_ELEMENTS_LIST:
        hll = HyperLogLogPlusPlus(b=10)
        data_stream = [str(random.randint(1, 1_000_000)) for _ in range(n)]

        tracemalloc.start()
        start = time.perf_counter()
        for item in data_stream:
            hll.update(item)
        end = time.perf_counter()
        _, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        avg_update_time = (end - start) / n * 1e6
        true_cardinality = len(set(data_stream))
        est_cardinality = hll.estimate()
        abs_error = abs(est_cardinality - true_cardinality)
        rel_error = abs_error / true_cardinality
        mem_usage_mb = peak_mem / (1024**2)

        writer.writerow([n, avg_update_time, true_cardinality, est_cardinality, abs_error, rel_error, mem_usage_mb])

