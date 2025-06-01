from structures.base import StreamEstimator

class SpaceSaving(StreamEstimator):
    """
    estructura para top-k elementos más frecuentes
    """

    def __init__(self, k: int = 10):
        if k < 1:
            raise ValueError("k debe ser al menos 1")
        self.k = k
        self.counters = {}   

    def update(self, item, count=1):
        
        if item in self.counters:
            freq, err = self.counters[item]
            self.counters[item] = (freq + count, err)
        elif len(self.counters) < self.k:
            self.counters[item] = (count, 0)
        else:
            min_item = min(self.counters, key=lambda x: self.counters[x][0])
            min_count, min_error = self.counters[min_item]

            del self.counters[min_item]
            self.counters[item] = (min_count + count, min_count)

    def estimate(self, item):
        return self.counters.get(item, (0, 0))[0]

    def consultar_top_k(self, k=None):
        k = k or self.k
        return sorted(self.counters.items(), key=lambda x: -x[1][0])[:k]

    def reset(self):
        self.counters = {}

    def __repr__(self):
        return f"<SpaceSaving k={self.k} counters={len(self.counters)}>"

    def get_memory_usage(self):
        import sys
        size = sys.getsizeof(self.counters)
        for k, (c, e) in self.counters.items():
            size += sys.getsizeof(k) + sys.getsizeof(c) + sys.getsizeof(e)
        return size
