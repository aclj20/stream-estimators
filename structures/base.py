from abc import ABC, abstractmethod

class StreamEstimator(ABC):

    @abstractmethod
    def update(self, item, count=1):
        """
        procesa una actualización del stream
        """
        pass

    @abstractmethod
    def estimate(self, item):
        """
        estima la respuesta a una consulta para un elemento específico
        """
        pass

    @abstractmethod
    def reset(self):
        """
        reinicia el estado interno del sketch a su estado inicial vacío
        """
        pass


    def get_memory_usage(self):
        """
        devuelve una estimación de la memoria usada por el sketch en bytes
        """
        raise NotImplementedError("Memory usage estimation not implemented.")
