from services.algoritmos import (
    asignar_first_fit,
    asignar_best_fit
)

from utils.metricas import calcular_metricas


# Distribución inicial de memoria: 1024 KB
memoria_inicial = [
    {"inicio": 0, "tamano": 300, "proceso": None},
    {"inicio": 300, "tamano": 100, "proceso": "P2"},
    {"inicio": 400, "tamano": 280, "proceso": None},
    {"inicio": 680, "tamano": 100, "proceso": "P4"},
    {"inicio": 780, "tamano": 244, "proceso": None}
]

memoria_total = 1024

# Tamaño del proceso que queremos asignar
proceso_id = "P3"
tamano_proceso = 250


# Ejecutar First Fit
memoria_ff, exito_ff = asignar_first_fit(
    [bloque.copy() for bloque in memoria_inicial],
    proceso_id,
    tamano_proceso
)


# Ejecutar Best Fit
memoria_bf, exito_bf = asignar_best_fit(
    [bloque.copy() for bloque in memoria_inicial],
    proceso_id,
    tamano_proceso
)


def mostrar_resultados(nombre, memoria, exito):

    print(f"\n========== {nombre} ==========")

    print("Asignación exitosa:", exito)

    for bloque in memoria:
        estado = bloque["proceso"] or "LIBRE"

        print(
            f"Inicio: {bloque['inicio']} KB | "
            f"Tamaño: {bloque['tamano']} KB | "
            f"Estado: {estado}"
        )

    metricas = calcular_metricas(memoria, memoria_total)

    print("\nMÉTRICAS:")

    for indicador, valor in metricas.items():
        print(f"{indicador}: {valor}")


# Mostrar ambos resultados
mostrar_resultados("FIRST FIT", memoria_ff, exito_ff)

mostrar_resultados("BEST FIT", memoria_bf, exito_bf)