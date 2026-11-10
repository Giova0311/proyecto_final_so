from services.algoritmos import (
    asignar_first_fit,
    asignar_best_fit
)

from utils.metricas import calcular_metricas


memoria_inicial = [
    {"inicio": 0, "tamano": 200, "proceso": None},
    {"inicio": 200, "tamano": 100, "proceso": "P1"},
    {"inicio": 300, "tamano": 300, "proceso": None},
    {"inicio": 600, "tamano": 100, "proceso": "P2"},
    {"inicio": 700, "tamano": 100, "proceso": None},
    {"inicio": 800, "tamano": 224, "proceso": "P3"}
]

solicitudes = [
    ("Q1", 90),
    ("Q2", 115),
    ("Q3", 190)
]


def ejecutar_escenario(nombre, algoritmo):

    memoria = [bloque.copy() for bloque in memoria_inicial]
    asignados = 0
    rechazados = 0

    print(f"\n========== {nombre} ==========")

    for proceso_id, tamano in solicitudes:

        if algoritmo == "first_fit":
            memoria, exito = asignar_first_fit(
                memoria, proceso_id, tamano
            )
        else:
            memoria, exito = asignar_best_fit(
                memoria, proceso_id, tamano
            )

        if exito:
            asignados += 1
            print(f"{proceso_id}: {tamano} KB - ASIGNADO")
        else:
            rechazados += 1
            print(f"{proceso_id}: {tamano} KB - RECHAZADO")

    metricas = calcular_metricas(memoria, 1024)

    print("\nRESUMEN:")
    print("Procesos asignados:", asignados)
    print("Procesos rechazados:", rechazados)

    for indicador, valor in metricas.items():
        print(f"{indicador}: {valor}")


ejecutar_escenario("FIRST FIT", "first_fit")
ejecutar_escenario("BEST FIT", "best_fit")