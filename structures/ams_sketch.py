import mmh3
from random import randint
from math import sqrt
from structures.base import StreamEstimator  # Nuestra interfaz

class AMSSketch(StreamEstimator):
    """
    Estima el segundo momento de un flujo de datos
    """

    def __init__(self, num_projections: int = 10, seed: int = None):
        """
        num_projections es el número de contadores
        """
        self.num_projections = num_projections
        self.seed = seed or randint(0, 1 << 30)
        self.counters = [0] * num_projections

    def _sign_hash(self, item, i):
        """
        genera un signo +/-1 para el ítem para cada contador i
        """
        combined_seed = self.seed + i
        h = mmh3.hash(str(item), combined_seed, signed=True)
        return 1 if (h & 1) == 0 else -1

    def update(self, item, count=1):
        for i in range(self.num_projections):
            sign = self._sign_hash(item, i)
            self.counters[i] += sign * count

    def estimate(self, item=None):
        """
        estimación del segundo momento
        """
        estimates = [(c ** 2) for c in self.counters]
        return sum(estimates) / self.num_projections

    def reset(self):
        self.counters = [0] * self.num_projections

    def __repr__(self):
        return f"<AMSSketch projections={self.num_projections} seed={self.seed}>"

    def get_memory_usage(self):
        import sys
        size = sys.getsizeof(self.counters)
        for c in self.counters:
            size += sys.getsizeof(c)
        return size
