
from services.algoritmos import (
    asignar_first_fit,
    asignar_best_fit
)


# Memoria inicial de 1024 KB
memoria = [
    {"inicio": 0, "tamano": 300, "proceso": None},
    {"inicio": 300, "tamano": 100, "proceso": "P1"},
    {"inicio": 400, "tamano": 280, "proceso": None},
    {"inicio": 680, "tamano": 100, "proceso": "P2"},
    {"inicio": 780, "tamano": 244, "proceso": None}
]


# Probar First Fit
resultado_ff, exito_ff = asignar_first_fit(
    memoria, "P3", 250
)

# Probar Best Fit
resultado_bf, exito_bf = asignar_best_fit(
    memoria, "P3", 250
)


# Mostrar resultados
print("\n========== FIRST FIT ==========")
print("Asignación exitosa:", exito_ff)

for bloque in resultado_ff:
    print(bloque)


print("\n========== BEST FIT ==========")
print("Asignación exitosa:", exito_bf)

for bloque in resultado_bf:
    print(bloque)
