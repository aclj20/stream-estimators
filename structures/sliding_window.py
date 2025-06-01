from collections import deque
from structures.base import StreamEstimator

class SlidingWindowAggregator(StreamEstimator):
    """
    Sliding Window Aggregator para mantener métricas de los últimos N elementos.
    """

    def __init__(self, window_size: int = 100):
        if window_size < 1:
            raise ValueError("window_size debe ser >= 1")
        self.window_size = window_size
        self.window = deque()
        self.sum = 0

    def update(self, item, count=1):
        """
        Inserta el ítem 'count' veces en la ventana.
        """
        for _ in range(count):
            self.window.append(item)
            self.sum += item
            if len(self.window) > self.window_size:
                removed = self.window.popleft()
                self.sum -= removed

    def estimate(self, item=None):
        """
        Retorna el promedio de los últimos N elementos.
        El parámetro 'item' se ignora.
        """
        if not self.window:
            return 0
        return self.sum / len(self.window)

    def consultar_ventana_deslizante(self):
        """
        Devuelve un resumen de la ventana: suma, promedio, tamaño actual.
        """
        return {
            "suma": self.sum,
            "promedio": self.sum / len(self.window) if self.window else 0,
            "size_actual": len(self.window),
            "maximo": max(self.window) if self.window else None,
            "minimo": min(self.window) if self.window else None
        }

    def reset(self):
        """
        Reinicia la ventana.
        """
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
