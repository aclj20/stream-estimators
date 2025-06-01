from collections import deque
from structures.base import StreamEstimator

class SlidingWindowAggregator(StreamEstimator):

    def __init__(self, window_size: int = 100):
        if window_size < 1:
            raise ValueError("window_size debe ser >= 1")
        self.window_size = window_size
        self.window = deque()
        self.sum = 0

    def update(self, item, count=1):
        for _ in range(count):
            self.window.append(item)
            self.sum += item
            if len(self.window) > self.window_size:
                removed = self.window.popleft()
                self.sum -= removed

    def estimate(self, item=None):
        if not self.window:
            return 0
        return self.sum / len(self.window)

    def consultar_ventana_deslizante(self):
        return {
            "suma": self.sum,
            "promedio": self.sum / len(self.window) if self.window else 0,
            "size_actual": len(self.window),
            "maximo": max(self.window) if self.window else None,
            "minimo": min(self.window) if self.window else None
        }

    def reset(self):
        self.window.clear()
        self.sum = 0

    def __repr__(self):
        return f"<SlidingWindowAggregator window_size={self.window_size} current_size={len(self.window)}>"

    def get_memory_usage(self):
        import sys
        size = sys.getsizeof(self.window)
        for item in self.window:
            size += sys.getsizeof(item)
        size += sys.getsizeof(self.sum)
        return size
