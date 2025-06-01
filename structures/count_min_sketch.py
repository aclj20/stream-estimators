import mmh3
import sys
from array import array
from math import ceil, e, log
from typing import Union

class CountMinSketch:

    def __init__(
        self,
        epsilon: float,
        delta: float,
        conservative: bool = False,
    ):
        # Validar rangos de parámetros
        if not (0 < epsilon < 1):
            raise ValueError(f"epsilon debe estar en (0,1), pero vino {epsilon}")
        if not (0 < delta < 1):
            raise ValueError(f"delta debe estar en (0,1), pero vino {delta}")

        self.epsilon = epsilon
        self.delta = delta
        self.conservative = conservative

        self.w = ceil(e / epsilon)
        self.d = ceil(log(1 / delta))
        self.total = 0                   

        self.table = [array('L', [0] * self.w) for _ in range(self.d)]

        self.seeds = [((i * 0xFBA4C795 + 1) & 0xFFFFFFFF) for i in range(self.d)]

    def update(self, key: Union[str, bytes], count: int = 1) -> None:
        if count < 1:
            raise ValueError(f"count debe ser >=1, pero vino {count}")

        indices = [mmh3.hash(str(key), seed) % self.w for seed in self.seeds]

        if self.conservative:
            valores = [self.table[i][idx] for i, idx in enumerate(indices)]
            minimo = min(valores)
            for i, idx in enumerate(indices):
                if self.table[i][idx] == minimo:
                    self.table[i][idx] += count
        else:
            for i, idx in enumerate(indices):
                self.table[i][idx] += count

        self.total += count

    def estimate(self, key: Union[str, bytes]) -> int:
        """
        devuelve la estimación de frecuencia de key
        """
        return min(
            self.table[i][mmh3.hash(key, seed) % self.w]
            for i, seed in enumerate(self.seeds)
        )

    def reset(self):
        self.total = 0
        for i in range(self.d):
            for j in range(self.w):
                self.table[i][j] = 0

    def __len__(self) -> int:
        return self.total
    
    def get_memory_usage(self):
        size = sys.getsizeof(self.table)
        for row in self.table:
            size += sys.getsizeof(row)
        size += sys.getsizeof(self.seeds)
        return size

    
    

    