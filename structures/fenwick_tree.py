from structures.base import StreamEstimator

class FenwickTree(StreamEstimator):
    """
    Fenwick Tree (Binary Indexed Tree) para acumulados eficientes.
    """

    def __init__(self, size: int):
        """
        :param size: tamaño máximo del arreglo (1-indexado internamente).
        """
        if size < 1:
            raise ValueError("size debe ser >= 1")
        self.n = size
        self.tree = [0] * (size + 1)  # 1-indexado

    def update(self, idx, delta=1):
        """
        Incrementa el valor en posición 'idx' en 'delta' (idx es 0-indexado externamente).
        """
        idx += 1  # convertimos a 1-indexado
        while idx <= self.n:
            self.tree[idx] += delta
            idx += idx & -idx

    def estimate(self, idx):
        """
        Devuelve la suma acumulada desde 0 hasta idx (inclusive).
        """
        idx += 1  # convertimos a 1-indexado
        result = 0
        while idx > 0:
            result += self.tree[idx]
            idx -= idx & -idx
        return result

    def consultar_acumulado_hasta(self, idx):
        """
        Sinónimo más explícito de 'estimate'.
        """
        return self.estimate(idx)

    def reset(self):
        """
        Reinicia la estructura.
        """
        self.tree = [0] * (self.n + 1)

    def __repr__(self):
        return f"<FenwickTree size={self.n}>"
    
    def get_memory_usage(self):
        import sys
        size = sys.getsizeof(self.tree)
        for item in self.tree:
            size += sys.getsizeof(item)
        return size

