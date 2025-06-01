from abc import ABC, abstractmethod

class StreamEstimator(ABC):
    """
    Interfaz base para todos los estimadores de streams de datos.
    
    Cada implementación debe:
    - Mantener un estado interno compacto (memoria sublineal).
    - Procesar flujos de datos de manera incremental.
    - Dar respuestas aproximadas, no exactas.
    """

    @abstractmethod
    def update(self, item, count=1):
        """
        Procesa una actualización del stream.
        
        Parámetros:
        - item: El elemento a procesar (puede ser cualquier objeto hashable).
        - count: Número de veces que aparece (default=1). Permite procesar múltiples ocurrencias de un ítem de golpe.
        """
        pass

    @abstractmethod
    def estimate(self, item):
        """
        Estima la respuesta a una consulta para un elemento específico.
        
        Ejemplo de consultas:
        - Frecuencia de aparición (Count-Min, Space-Saving).
        - Inclusión (Bloom, no tu caso).
        - Cardinalidad de conjunto (HyperLogLog++).
        - Momento de orden 2 (AMS Sketch).
        
        Parámetros:
        - item: Elemento a consultar.
        
        Retorna:
        - Una estimación numérica (ej: frecuencia, probabilidad, cardinalidad, etc.).
        """
        pass

    @abstractmethod
    def reset(self):
        """
        Reinicia el estado interno del sketch a su estado inicial vacío.
        """
        pass

    def merge(self, other):
        """
        (Opcional) Mezcla el estado de otro sketch compatible.
        
        Algunos algoritmos permiten la fusión de dos sketches (ej: HyperLogLog++, Count-Min Sketch con misma configuración).
        Parámetros:
        - other: Otro sketch del mismo tipo.
        
        Lanza:
        - NotImplementedError si la fusión no es compatible.
        """
        raise NotImplementedError("Merge not supported for this sketch.")

    def get_memory_usage(self):
        """
        (Opcional) Devuelve una estimación de la memoria usada por el sketch en bytes.
        Ideal para comparaciones de eficiencia entre algoritmos.
        
        Retorna:
        - Entero (bytes).
        """
        raise NotImplementedError("Memory usage estimation not implemented.")
