from structures.count_min_sketch import CountMinSketch
from structures.hyperloglogpp import HyperLogLogPlusPlus
from structures.stream_summary import SpaceSaving
from structures.ams_sketch import AMSSketch
from structures.fenwick_tree import FenwickTree
from structures.sliding_window import SlidingWindowAggregator

class StreamEstimatorManager:
    """
    Coordinador de sketches para procesamiento de streams con memoria limitada.
    """

    def __init__(self, **kwargs):
        """
        Inicializa todos los sketches internos con parámetros opcionales.
        Puedes pasar:
        - cms_epsilon, cms_delta
        - hll_b
        - ss_k
        - ams_projections
        - fenwick_size
        - window_size
        """
        # Inicializar cada sketch con parámetros personalizados o por defecto
        self.cms = CountMinSketch(
            epsilon=kwargs.get("cms_epsilon", 0.01),
            delta=kwargs.get("cms_delta", 0.01)
        )
        self.hll = HyperLogLogPlusPlus(
            b=kwargs.get("hll_b", 12)
        )
        self.ss = SpaceSaving(
            k=kwargs.get("ss_k", 10)
        )
        self.ams = AMSSketch(
            num_projections=kwargs.get("ams_projections", 10)
        )
        self.fenwick = FenwickTree(
            size=kwargs.get("fenwick_size", 1000)
        )
        self.sliding = SlidingWindowAggregator(
            window_size=kwargs.get("window_size", 100)
        )

    def update(self, item, count=1):
        """
        Actualiza todos los sketches internos con el ítem y su conteo.
        """
        # Count–Min Sketch
        self.cms.update(item, count)
        # HyperLogLog++ (ignora count)
        self.hll.update(item)
        # Space-Saving
        self.ss.update(item, count)
        # AMS Sketch
        self.ams.update(item, count)
        # Fenwick Tree (usamos el ítem como índice si es int)
        if isinstance(item, int):
            self.fenwick.update(item, count)
        # Sliding Window Aggregator
        if isinstance(item, (int, float)):
            self.sliding.update(item, count)

    def consultar_frecuencia(self, item):
        """
        Devuelve la frecuencia aproximada de un ítem.
        """
        return self.cms.estimate(item)

    def consultar_unicidad(self):
        """
        Devuelve la cardinalidad aproximada.
        """
        return self.hll.estimate()

    def consultar_top_k(self, k=10):
        """
        Devuelve los 'k' ítems más frecuentes.
        """
        return self.ss.consultar_top_k(k)

    def consultar_varianza(self):
        """
        Devuelve la estimación del segundo momento (varianza).
        """
        return self.ams.estimate()

    def consultar_acumulado_hasta(self, item):
        """
        Devuelve la suma acumulada hasta el índice 'item'.
        """
        return self.fenwick.consultar_acumulado_hasta(item)

    def consultar_ventana_deslizante(self):
        """
        Devuelve el resumen de la ventana.
        """
        return self.sliding.consultar_ventana_deslizante()

    def reset(self):
        """
        Reinicia todos los sketches.
        """
        self.cms.reset()
        self.hll.reset()
        self.ss.reset()
        self.ams.reset()
        self.fenwick.reset()
        self.sliding.reset()

    def get_memory_usage(self):
        """
        Devuelve un diccionario con el uso de memoria estimado por cada sketch.
        """
        return {
            "CountMinSketch": self.cms.get_memory_usage(),
            "HyperLogLog++": self.hll.get_memory_usage(),
            "SpaceSaving": self.ss.get_memory_usage(),
            "AMSSketch": self.ams.get_memory_usage(),
            "FenwickTree": self.fenwick.get_memory_usage(),
            "SlidingWindowAggregator": self.sliding.get_memory_usage()
        }

