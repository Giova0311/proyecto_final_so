"""
Escenario 4: secuencia larga de asignaciones y liberaciones.

A diferencia de los escenarios 1-3 (que parten de una memoria ya
fragmentada a mano), aquí la fragmentación se produce de forma natural
a partir de una secuencia pseudoaleatoria de operaciones sobre una
memoria que inicia vacía.

Reproducibilidad: cada ejecución usa una semilla fija. Para una misma
semilla, First Fit y Best Fit reciben EXACTAMENTE la misma secuencia.

Ejecutar desde la carpeta backend:
    python -m tests.escenario_4_secuencia_larga
"""
import os
import random
import statistics

from services.simulador import SimuladorMemoria
from utils.metricas import calcular_metricas

MEMORIA_TOTAL = 1024
NUM_OPERACIONES = 300
TAMANO_MIN, TAMANO_MAX = 20, 120
PROB_ASIGNAR = 0.50
SEMILLAS = list(range(1, 21))  # 20 secuencias distintas pero reproducibles


def generar_secuencia(semilla):
    """Genera la lista de operaciones. No depende del algoritmo."""
    rng = random.Random(semilla)
    operaciones = []
    creados = []
    contador = 0

    for _ in range(NUM_OPERACIONES):
        if creados and rng.random() > PROB_ASIGNAR:
            proceso = creados.pop(rng.randrange(len(creados)))
            operaciones.append(("liberar", proceso, None))
        else:
            contador += 1
            proceso = f"P{contador}"
            creados.append(proceso)
            operaciones.append(
                ("asignar", proceso, rng.randint(TAMANO_MIN, TAMANO_MAX))
            )
    return operaciones


def ejecutar(operaciones, algoritmo):
    sim = SimuladorMemoria(MEMORIA_TOTAL)
    asignados = rechazados = 0
    uso, frag, mayor = [], [], []

    for tipo, proceso, tamano in operaciones:
        if tipo == "asignar":
            exito, _ = sim.asignar_proceso(proceso, tamano, algoritmo)
            if exito:
                asignados += 1
            else:
                rechazados += 1
        else:
            # Si el proceso fue rechazado antes, no está en memoria y se ignora
            sim.liberar_proceso(proceso)

        m = calcular_metricas(sim.obtener_memoria(), MEMORIA_TOTAL)
        uso.append(m["porcentaje_uso"])
        frag.append(m["fragmentacion_externa"])
        mayor.append(m["bloque_libre_mayor"])

    # Invariante: la suma de bloques siempre es la memoria total
    assert sum(b["tamano"] for b in sim.obtener_memoria()) == MEMORIA_TOTAL

    return {
        "asignados": asignados,
        "rechazados": rechazados,
        "uso_prom": statistics.mean(uso),
        "frag_prom": statistics.mean(frag),
        "frag_max": max(frag),
        "mayor_prom": statistics.mean(mayor),
    }


def main():
    lineas = []

    def out(texto=""):
        print(texto)
        lineas.append(texto)

    out("=== ESCENARIO 4: SECUENCIA LARGA (asignar/liberar) ===")
    out(f"Memoria: {MEMORIA_TOTAL} KB | Operaciones por secuencia: "
        f"{NUM_OPERACIONES} | Tamaños: {TAMANO_MIN}-{TAMANO_MAX} KB | "
        f"P(asignar)={PROB_ASIGNAR}")
    out(f"Secuencias (semillas): {SEMILLAS[0]}..{SEMILLAS[-1]}")
    out()
    out(f"{'Sem':>3} | {'Algoritmo':<9} | {'Asig':>4} | {'Rech':>4} | "
        f"{'Uso%':>6} | {'Frag%':>6} | {'FragMax%':>8} | {'MayorKB':>7}")
    out("-" * 68)

    resultados = {"first_fit": [], "best_fit": []}

    for semilla in SEMILLAS:
        ops = generar_secuencia(semilla)
        for alg in ("first_fit", "best_fit"):
            r = ejecutar(ops, alg)
            resultados[alg].append(r)
            out(f"{semilla:>3} | {alg:<9} | {r['asignados']:>4} | "
                f"{r['rechazados']:>4} | {r['uso_prom']:>6.2f} | "
                f"{r['frag_prom']:>6.2f} | {r['frag_max']:>8.2f} | "
                f"{r['mayor_prom']:>7.1f}")

    out()
    out("=== PROMEDIO SOBRE TODAS LAS SECUENCIAS ===")
    out(f"{'Algoritmo':<10} | {'Rechaz.':>7} | {'Uso%':>6} | "
        f"{'Frag%':>6} | {'MayorKB':>7}")
    out("-" * 50)
    for alg, lista in resultados.items():
        out(f"{alg:<10} | "
            f"{statistics.mean(r['rechazados'] for r in lista):>7.2f} | "
            f"{statistics.mean(r['uso_prom'] for r in lista):>6.2f} | "
            f"{statistics.mean(r['frag_prom'] for r in lista):>6.2f} | "
            f"{statistics.mean(r['mayor_prom'] for r in lista):>7.1f}")

    mejor = sum(
        1 for a, b in zip(resultados["first_fit"], resultados["best_fit"])
        if b["rechazados"] < a["rechazados"]
    )
    peor = sum(
        1 for a, b in zip(resultados["first_fit"], resultados["best_fit"])
        if b["rechazados"] > a["rechazados"]
    )
    out()
    out(f"Secuencias donde Best Fit rechazó MENOS que First Fit: {mejor}")
    out(f"Secuencias donde Best Fit rechazó MÁS que First Fit:  {peor}")
    out(f"Empates: {len(SEMILLAS) - mejor - peor}")

    # Guardar evidencia
    ruta = os.path.join(os.path.dirname(__file__), "..", "..",
                        "evidencias", "resultados_escenario_4.txt")
    ruta = os.path.abspath(ruta)
    try:
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("\n".join(lineas) + "\n")
        print(f"\nResultados guardados en: {ruta}")
    except OSError as e:
        print(f"\nNo se pudo guardar el archivo de evidencia: {e}")


if __name__ == "__main__":
    main()
