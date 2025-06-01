import mmh3
import math
from structures.base import StreamEstimator  

class HyperLogLogPlusPlus(StreamEstimator):
    """
    HyperLogLog++ adaptado para la librería: estima cardinalidad de un flujo.
    Usa representación dispersa (sparse) y densa (dense) de manera automática.
    """

    def __init__(self, b: int = 12):
        if not (4 <= b <= 16):
            raise ValueError("b debe estar en [4,16]")
        self.b = b
        self.m = 1 << b
        self.alpha = 0.7213 / (1 + 1.079 / self.m)
        self._w_bits = 64 - b

        self.sparse = {}
        self.dense = None

    def _rho(self, w: int) -> int:
        if w == 0:
            return self._w_bits + 1
        return (self._w_bits - w.bit_length()) + 1

    def _hash(self, value: str) -> int:
        return mmh3.hash64(value.encode('utf-8'), signed=False)[0]

    def update(self, item, count=1):
        """
        Inserta el ítem en el sketch.
        El parámetro 'count' se ignora (no tiene sentido en cardinalidad).
        """
        x = self._hash(item)
        idx = x >> self._w_bits
        w = x & ((1 << self._w_bits) - 1)
        rho = self._rho(w)

        if self.dense is not None:
            self.dense[idx] = max(self.dense[idx], rho)
        else:
            if idx not in self.sparse or rho > self.sparse[idx]:
                self.sparse[idx] = rho
            if len(self.sparse) > (self.m / 2):
                self._convert_to_dense()

    def _convert_to_dense(self):
        self.dense = [0] * self.m
        for idx, val in self.sparse.items():
            self.dense[idx] = val
        self.sparse = None

    def estimate(self, item=None) -> float:
        """
        Estima la cardinalidad global del flujo.
        El parámetro 'item' se ignora.
        """
        if self.dense is not None:
            registers = self.dense
        else:
            V = self.m - len(self.sparse)
            if V > 0:
                return self.m * math.log(self.m / V)
            registers = [0] * self.m
            for idx, val in self.sparse.items():
                registers[idx] = val

        Z = 1.0 / sum(2.0 ** -r for r in registers)
        E = self.alpha * self.m * self.m * Z

        if E > (1/30) * (1 << 64):
            E = - (1 << 64) * math.log(1 - E / (1 << 64))

        return E

    def reset(self):
        """
        Reinicia el estado interno del sketch.
        """
        self.sparse = {}
        self.dense = None

    def get_memory_usage(self):
        import sys
        size = sys.getsizeof(self)
        if self.dense is not None:
            size += sys.getsizeof(self.dense)
        else:
            size += sys.getsizeof(self.sparse)
            for k, v in self.sparse.items():
                size += sys.getsizeof(k) + sys.getsizeof(v)
        return size
