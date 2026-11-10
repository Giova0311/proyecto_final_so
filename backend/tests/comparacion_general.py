from services.algoritmos import (
    asignar_first_fit,
    asignar_best_fit
)
from utils.metricas import calcular_metricas


ESCENARIOS = [
    {
        "nombre": "Escenario 1",
        "memoria": [
            {"inicio": 0, "tamano": 300, "proceso": None},
            {"inicio": 300, "tamano": 100, "proceso": "P2"},
            {"inicio": 400, "tamano": 280, "proceso": None},
            {"inicio": 680, "tamano": 100, "proceso": "P4"},
            {"inicio": 780, "tamano": 244, "proceso": None}
        ],
        "solicitudes": [("P3", 250)]
    },
    {
        "nombre": "Escenario 2",
        "memoria": [
            {"inicio": 0, "tamano": 200, "proceso": None},
            {"inicio": 200, "tamano": 100, "proceso": "P1"},
            {"inicio": 300, "tamano": 300, "proceso": None},
            {"inicio": 600, "tamano": 100, "proceso": "P2"},
            {"inicio": 700, "tamano": 100, "proceso": None},
            {"inicio": 800, "tamano": 224, "proceso": "P3"}
        ],
        "solicitudes": [
            ("Q1", 90),
            ("Q2", 115),
            ("Q3", 190)
        ]
    },
    {
        "nombre": "Escenario 3",
        "memoria": [
            {"inicio": 0, "tamano": 150, "proceso": None},
            {"inicio": 150, "tamano": 100, "proceso": "P1"},
            {"inicio": 250, "tamano": 100, "proceso": None},
            {"inicio": 350, "tamano": 100, "proceso": "P2"},
            {"inicio": 450, "tamano": 200, "proceso": None},
            {"inicio": 650, "tamano": 374, "proceso": "P3"}
        ],
        "solicitudes": [("Q1", 250)]
    }
]


def ejecutar_escenario(escenario, nombre_algoritmo):

    memoria = [
        bloque.copy()
        for bloque in escenario["memoria"]
    ]

    asignar = (
        asignar_first_fit
        if nombre_algoritmo == "First Fit"
        else asignar_best_fit
    )

    asignados = 0
    rechazados = 0

    for proceso_id, tamano in escenario["solicitudes"]:

        memoria, exito = asignar(
            memoria,
            proceso_id,
            tamano
        )

        if exito:
            asignados += 1
        else:
            rechazados += 1

    metricas = calcular_metricas(memoria, 1024)

    return {
        "asignados": asignados,
        "rechazados": rechazados,
        "utilizacion": metricas["porcentaje_uso"],
        "fragmentacion": metricas["fragmentacion_externa"],
        "bloque_mayor": metricas["bloque_libre_mayor"]
    }


print("\n========== COMPARACIÓN GENERAL ==========\n")

for escenario in ESCENARIOS:

    first_fit = ejecutar_escenario(escenario, "First Fit")
    best_fit = ejecutar_escenario(escenario, "Best Fit")

    print(escenario["nombre"])

    print(
        f"First Fit: asignados={first_fit['asignados']}, "
        f"rechazados={first_fit['rechazados']}, "
        f"utilización={first_fit['utilizacion']}%, "
        f"fragmentación={first_fit['fragmentacion']}%"
    )

    print(
        f"Best Fit:  asignados={best_fit['asignados']}, "
        f"rechazados={best_fit['rechazados']}, "
        f"utilización={best_fit['utilizacion']}%, "
        f"fragmentación={best_fit['fragmentacion']}%"
    )

    print("-" * 65)