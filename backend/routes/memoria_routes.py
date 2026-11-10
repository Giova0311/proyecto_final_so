from flask import Blueprint, jsonify, request

from services.simulador import SimuladorMemoria
from utils.metricas import calcular_metricas
from services.algoritmos import (
    asignar_first_fit,
    asignar_best_fit
)


memoria_bp = Blueprint("memoria", __name__)

# Simulador compartido por todas las solicitudes
simulador = SimuladorMemoria(1024)


def obtener_estado():
    memoria = simulador.obtener_memoria()

    return {
        "memoria": memoria,
        "metricas": calcular_metricas(
            memoria,
            simulador.memoria_total
        )
    }


# Consultar el estado de la memoria
@memoria_bp.route("/api/memoria", methods=["GET"])
def consultar_memoria():
    return jsonify(obtener_estado())


# Crear y asignar un proceso
@memoria_bp.route("/api/procesos", methods=["POST"])
def crear_proceso():

    datos = request.get_json(silent=True) or {}

    proceso_id = datos.get("proceso_id")
    tamano = datos.get("tamano")
    algoritmo = datos.get("algoritmo")

    if not isinstance(proceso_id, str) or not proceso_id.strip():
        return jsonify({"error": "Identificador de proceso no válido."}), 400

    if not isinstance(tamano, int) or isinstance(tamano, bool) or tamano <= 0:
        return jsonify({"error": "El tamaño debe ser un entero positivo."}), 400

    if algoritmo not in ["first_fit", "best_fit"]:
        return jsonify({"error": "Algoritmo no válido."}), 400

    exito, mensaje = simulador.asignar_proceso(
        proceso_id.strip(),
        tamano,
        algoritmo
    )

    if not exito:
        return jsonify({"error": mensaje}), 409

    return jsonify({
        "mensaje": mensaje,
        **obtener_estado()
    })


# Liberar un proceso
@memoria_bp.route("/api/procesos/<proceso_id>", methods=["DELETE"])
def eliminar_proceso(proceso_id):

    exito, mensaje = simulador.liberar_proceso(proceso_id)

    if not exito:
        return jsonify({"error": mensaje}), 404

    return jsonify({
        "mensaje": mensaje,
        **obtener_estado()
    })


# Reiniciar la memoria
@memoria_bp.route("/api/memoria/reiniciar", methods=["POST"])
def reiniciar_memoria():

    global simulador

    datos = request.get_json(silent=True) or {}
    memoria_total = datos.get("memoria_total", 1024)

    if (
        not isinstance(memoria_total, int)
        or isinstance(memoria_total, bool)
        or memoria_total <= 0
    ):
        return jsonify({
            "error": "La memoria total debe ser un entero positivo."
        }), 400

    simulador = SimuladorMemoria(memoria_total)

    return jsonify({
        "mensaje": "Memoria reiniciada correctamente.",
        **obtener_estado()
    })
    
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


def ejecutar_experimento(escenario, algoritmo):

    memoria = [
        bloque.copy()
        for bloque in escenario["memoria"]
    ]

    funcion = (
        asignar_first_fit
        if algoritmo == "first_fit"
        else asignar_best_fit
    )

    asignados = 0
    rechazados = 0

    for proceso_id, tamano in escenario["solicitudes"]:

        memoria, exito = funcion(
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
        "memoria_ocupada": metricas["memoria_ocupada"],
        "memoria_libre": metricas["memoria_libre"],
        "utilizacion": metricas["porcentaje_uso"],
        "fragmentacion": metricas["fragmentacion_externa"],
        "bloque_libre_mayor": metricas["bloque_libre_mayor"]
    }


@memoria_bp.route("/api/comparacion", methods=["POST"])
def comparar_algoritmos():

    resultados = []

    for escenario in ESCENARIOS:

        resultados.append({
            "escenario": escenario["nombre"],
            "first_fit": ejecutar_experimento(
                escenario, "first_fit"
            ),
            "best_fit": ejecutar_experimento(
                escenario, "best_fit"
            )
        })

    return jsonify({
        "resultados": resultados
    })