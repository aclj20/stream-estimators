import random
from structures.stream_estimator_manager import StreamEstimatorManager

def main():
    manager = StreamEstimatorManager(
        epsilon=0.01,
        delta=0.01,
        k=10,
        window_size=1000,
        num_hashes=5
    )

    NUM_ITEMS = 1_000_000
    print("Insertar 1 millón de claves")

    # Generar claves al azar
    keys = [str(random.randint(1, 10_000)) for _ in range(NUM_ITEMS)]
    
    # Insertar claves
    for key in keys:
        manager.update(key)

    print("Consultas a la librería")
    
    # Frecuencia aproximada
    test_key = keys[0]
    freq = manager.consultar_frecuencia(test_key)
    print(f"Frecuencia aproximada de '{test_key}': {freq}")

    # Estimación de elementos únicos
    uniq = manager.consultar_unicidad()
    print(f"Número de elementos únicos aproximado: {uniq}")

    # Top-k
    top_k = manager.consultar_top_k(10)
    print("Top 10 elementos más frecuentes:")
    for item, count in top_k:
        print(f"  {item}: {count}")

    # Estimación del segundo momento (varianza)
    varianza = manager.consultar_varianza()
    print(f"Segundo momento (varianza): {varianza}")

    # Estadísticas de la ventana deslizante
    ventana = manager.consultar_ventana_deslizante()
    print("Ventana deslizante:")
    for k, v in ventana.items():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    main()
