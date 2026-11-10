from services.algoritmos import (
    asignar_first_fit,
    asignar_best_fit
)


class SimuladorMemoria:

    def __init__(self, memoria_total=1024):
        self.memoria_total = memoria_total
        self.memoria = [
            {
                "inicio": 0,
                "tamano": memoria_total,
                "proceso": None
            }
        ]

    def asignar_proceso(self, proceso_id, tamano, algoritmo):

        if tamano <= 0:
            return False, "El tamaño debe ser mayor que cero."

        if any(b["proceso"] == proceso_id for b in self.memoria):
            return False, "El proceso ya existe en memoria."

        if algoritmo == "first_fit":
            nueva_memoria, exito = asignar_first_fit(
                self.memoria, proceso_id, tamano
            )

        elif algoritmo == "best_fit":
            nueva_memoria, exito = asignar_best_fit(
                self.memoria, proceso_id, tamano
            )

        else:
            return False, "Algoritmo no válido."

        if not exito:
            return False, "No hay un bloque libre suficiente."

        self.memoria = nueva_memoria
        return True, "Proceso asignado correctamente."

    def liberar_proceso(self, proceso_id):

        encontrado = False

        for bloque in self.memoria:
            if bloque["proceso"] == proceso_id:
                bloque["proceso"] = None
                encontrado = True

        if not encontrado:
            return False, "No se encontró el proceso."

        self._unir_bloques_libres()
        return True, "Memoria liberada correctamente."

    def _unir_bloques_libres(self):

        memoria_unida = []

        for bloque in self.memoria:

            if (
                memoria_unida
                and memoria_unida[-1]["proceso"] is None
                and bloque["proceso"] is None
            ):
                memoria_unida[-1]["tamano"] += bloque["tamano"]

            else:
                memoria_unida.append(bloque.copy())

        self.memoria = memoria_unida

        # Recalcular las posiciones de los bloques
        posicion = 0

        for bloque in self.memoria:
            bloque["inicio"] = posicion
            posicion += bloque["tamano"]

    def obtener_memoria(self):
        return self.memoria