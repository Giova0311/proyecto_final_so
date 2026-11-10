def calcular_metricas(memoria, memoria_total):

    memoria_ocupada = sum(
        bloque["tamano"]
        for bloque in memoria
        if bloque["proceso"] is not None
    )

    memoria_libre = memoria_total - memoria_ocupada

    bloques_libres = [
        bloque["tamano"]
        for bloque in memoria
        if bloque["proceso"] is None
    ]

    cantidad_bloques_libres = len(bloques_libres)

    bloque_libre_mayor = max(bloques_libres, default=0)

    porcentaje_uso = (
        memoria_ocupada / memoria_total * 100
        if memoria_total > 0 else 0
    )

    if memoria_libre > 0:
        fragmentacion_externa = (
            (memoria_libre - bloque_libre_mayor)
            / memoria_libre
        ) * 100
    else:
        fragmentacion_externa = 0

    return {
        "memoria_total": memoria_total,
        "memoria_ocupada": memoria_ocupada,
        "memoria_libre": memoria_libre,
        "porcentaje_uso": round(porcentaje_uso, 2),
        "cantidad_bloques_libres": cantidad_bloques_libres,
        "bloque_libre_mayor": bloque_libre_mayor,
        "fragmentacion_externa": round(fragmentacion_externa, 2)
    }