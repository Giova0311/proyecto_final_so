
def asignar_first_fit(memoria, proceso_id, tamano):
    """
    First Fit:
    Busca desde el inicio el primer bloque libre
    que tenga espacio suficiente.
    """

    for i, bloque in enumerate(memoria):

        if bloque["proceso"] is None and bloque["tamano"] >= tamano:

            memoria_nueva = [b.copy() for b in memoria]

            inicio = bloque["inicio"]
            espacio_restante = bloque["tamano"] - tamano

            # Asignar memoria al proceso
            memoria_nueva[i] = {
                "inicio": inicio,
                "tamano": tamano,
                "proceso": proceso_id
            }

            # Crear bloque libre si sobra espacio
            if espacio_restante > 0:
                memoria_nueva.insert(i + 1, {
                    "inicio": inicio + tamano,
                    "tamano": espacio_restante,
                    "proceso": None
                })

            return memoria_nueva, True

    return memoria, False


def asignar_best_fit(memoria, proceso_id, tamano):
    """
    Best Fit:
    Busca el bloque libre más pequeño
    que pueda almacenar el proceso.
    """

    mejor_indice = None
    mejor_tamano = None

    for i, bloque in enumerate(memoria):

        if bloque["proceso"] is None and bloque["tamano"] >= tamano:

            if mejor_tamano is None or bloque["tamano"] < mejor_tamano:
                mejor_tamano = bloque["tamano"]
                mejor_indice = i

    if mejor_indice is None:
        return memoria, False

    memoria_nueva = [b.copy() for b in memoria]

    bloque = memoria[mejor_indice]

    inicio = bloque["inicio"]
    espacio_restante = bloque["tamano"] - tamano

    # Asignar memoria al proceso
    memoria_nueva[mejor_indice] = {
        "inicio": inicio,
        "tamano": tamano,
        "proceso": proceso_id
    }

    # Crear bloque libre si sobra espacio
    if espacio_restante > 0:
        memoria_nueva.insert(mejor_indice + 1, {
            "inicio": inicio + tamano,
            "tamano": espacio_restante,
            "proceso": None
        })

    return memoria_nueva, True
