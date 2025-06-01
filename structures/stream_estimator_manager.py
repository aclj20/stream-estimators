from structures.count_min_sketch import CountMinSketch
from structures.hyperloglogpp import HyperLogLogPlusPlus
from structures.stream_summary import SpaceSaving
from structures.ams_sketch import AMSSketch
from structures.sliding_window import SlidingWindowAggregator

class StreamEstimatorManager:
    """
    Coordinador de sketches para procesamiento de streams con memoria limitada.
    """

    def __init__(self, **kwargs):
        """
        inicializa todos los sketches internos con parámetros opcionales
        """
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
        self.sliding = SlidingWindowAggregator(
            window_size=kwargs.get("window_size", 100)
        )

    def update(self, item, count=1):
 
        self.cms.update(item, count)

        self.hll.update(item)

        self.ss.update(item, count)

        self.ams.update(item, count)
        
        try:
            num_item = int(item)
            self.sliding.update(num_item, count)
        except ValueError:
            pass

    def consultar_frecuencia(self, item):
        return self.cms.estimate(item)

    def consultar_unicidad(self):
        return self.hll.estimate()

    def consultar_top_k(self, k=10):
        return self.ss.consultar_top_k(k)

    def consultar_varianza(self):
        return self.ams.estimate()


    def consultar_ventana_deslizante(self):
        return self.sliding.consultar_ventana_deslizante()

    def reset(self):
   
        self.cms.reset()
        self.hll.reset()
        self.ss.reset()
        self.ams.reset()
        self.sliding.reset()

    def get_memory_usage(self):
        return {
            "CountMinSketch": self.cms.get_memory_usage(),
            "HyperLogLog++": self.hll.get_memory_usage(),
            "SpaceSaving": self.ss.get_memory_usage(),
            "AMSSketch": self.ams.get_memory_usage(),
            "SlidingWindowAggregator": self.sliding.get_memory_usage()
        }

