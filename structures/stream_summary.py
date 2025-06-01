from structures.base import StreamEstimator

class SpaceSaving(StreamEstimator):
    """
    Space-Saving: estructura para top-k elementos más frecuentes.
    Mantiene solo k contadores.
    """

    def __init__(self, k: int = 10):
        if k < 1:
            raise ValueError("k debe ser al menos 1")
        self.k = k
        self.counters = {}   # item -> (count, error)

    def update(self, item, count=1):
        """
        Procesa la llegada de 'count' ocurrencias de 'item'.
        """
        if item in self.counters:
            freq, err = self.counters[item]
            self.counters[item] = (freq + count, err)
        elif len(self.counters) < self.k:
            self.counters[item] = (count, 0)
        else:
            # Reemplaza el ítem menos frecuente
            min_item = min(self.counters, key=lambda x: self.counters[x][0])
            min_count, min_error = self.counters[min_item]
            # Lo eliminamos y agregamos el nuevo ítem con margen de error
            del self.counters[min_item]
            self.counters[item] = (min_count + count, min_count)

    def estimate(self, item):
        """
        Devuelve la frecuencia aproximada de 'item'.
        Si no está, retorna 0.
        """
        return self.counters.get(item, (0, 0))[0]

    def consultar_top_k(self, k=None):
        """
        Devuelve los k ítems más frecuentes con sus conteos aproximados.
        """
        k = k or self.k
        return sorted(self.counters.items(), key=lambda x: -x[1][0])[:k]

    def reset(self):
        """
        Reinicia la estructura.
        """
        self.counters = {}

    def __repr__(self):
        return f"<SpaceSaving k={self.k} counters={len(self.counters)}>"

    def get_memory_usage(self):
        import sys
        size = sys.getsizeof(self.counters)
        for k, (c, e) in self.counters.items():
            size += sys.getsizeof(k) + sys.getsizeof(c) + sys.getsizeof(e)
        return size
