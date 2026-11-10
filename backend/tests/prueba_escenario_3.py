from services.algoritmos import (
    asignar_first_fit,
    asignar_best_fit
)

from utils.metricas import calcular_metricas


memoria_inicial = [
    {"inicio": 0, "tamano": 150, "proceso": None},
    {"inicio": 150, "tamano": 100, "proceso": "P1"},
    {"inicio": 250, "tamano": 100, "proceso": None},
    {"inicio": 350, "tamano": 100, "proceso": "P2"},
    {"inicio": 450, "tamano": 200, "proceso": None},
    {"inicio": 650, "tamano": 374, "proceso": "P3"}
]

memoria_total = 1024
proceso_id = "Q1"
tamano_proceso = 250


def ejecutar_escenario(nombre, algoritmo):

    memoria = [bloque.copy() for bloque in memoria_inicial]

    if algoritmo == "first_fit":
        memoria, exito = asignar_first_fit(
            memoria, proceso_id, tamano_proceso
        )
    else:
        memoria, exito = asignar_best_fit(
            memoria, proceso_id, tamano_proceso
        )

    print(f"\n========== {nombre} ==========")

    print("Asignación exitosa:", exito)

    if not exito:
        print("Motivo: no existe un bloque contiguo suficiente.")

    metricas = calcular_metricas(memoria, memoria_total)

    print("\nMÉTRICAS:")

    for indicador, valor in metricas.items():
        print(f"{indicador}: {valor}")


ejecutar_escenario("FIRST FIT", "first_fit")
ejecutar_escenario("BEST FIT", "best_fit")