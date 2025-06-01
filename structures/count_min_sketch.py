import mmh3
import sys
from array import array
from math import ceil, e, log
from typing import Union

class CountMinSketch:
    """
    Estructura probabilística Count–Min Sketch para estimar frecuencias.

    Parámetros
    ----------
    epsilon : float
        Fracción de error permitido (error aditivo máximo = epsilon * total_eventos).
    delta : float
        Probabilidad máxima de que el error exceda epsilon * total_eventos.
    conservative : bool, opcional
        Si es True, usa actualización conservadora para reducir la sobreestimación.
    """
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

        # Guardar parámetros
        self.epsilon = epsilon
        self.delta = delta
        self.conservative = conservative

        # Dimensiones: ancho w y número de filas d
        self.w = ceil(e / epsilon)
        self.d = ceil(log(1 / delta))
        self.total = 0                   # contador total de todos los eventos

        # Matriz d×w inicializada a ceros
        self.table = [array('L', [0] * self.w) for _ in range(self.d)]

        # Semillas de 32 bits para cada función de hash
        self.seeds = [((i * 0xFBA4C795 + 1) & 0xFFFFFFFF) for i in range(self.d)]

    def update(self, key: Union[str, bytes], count: int = 1) -> None:
        """
        Incrementa la cuenta de `key` en `count` (debe ser >=1).
        """
        if count < 1:
            raise ValueError(f"count debe ser >=1, pero vino {count}")

        # Calcular los índices en cada fila
        indices = [mmh3.hash(key, seed) % self.w for seed in self.seeds]

        if self.conservative:
            # Actualización conservadora: sólo incrementa las celdas con el valor mínimo actual
            valores = [self.table[i][idx] for i, idx in enumerate(indices)]
            minimo = min(valores)
            for i, idx in enumerate(indices):
                if self.table[i][idx] == minimo:
                    self.table[i][idx] += count
        else:
            # Actualización normal: incrementa todas las filas
            for i, idx in enumerate(indices):
                self.table[i][idx] += count

        self.total += count

    def estimate(self, key: Union[str, bytes]) -> int:
        """
        Devuelve la estimación de frecuencia de `key`.
        """
        return min(
            self.table[i][mmh3.hash(key, seed) % self.w]
            for i, seed in enumerate(self.seeds)
        )

    def reset(self):
        """
        Reinicia la estructura a estado inicial.
        """
        self.total = 0
        for i in range(self.d):
            for j in range(self.w):
                self.table[i][j] = 0

    def __len__(self) -> int:
        """
        Devuelve el conteo total de todos los elementos procesados.
        """
        return self.total
    
    def get_memory_usage(self):
        size = sys.getsizeof(self.table)
        for row in self.table:
            size += sys.getsizeof(row)
        size += sys.getsizeof(self.seeds)
        return size

    
    

    