from services.simulador import SimuladorMemoria


simulador = SimuladorMemoria(1024)

def mostrar_memoria():
    print("\nESTADO ACTUAL DE LA MEMORIA")
    print("-" * 45)

    for bloque in simulador.obtener_memoria():
        estado = bloque["proceso"] or "LIBRE"

        print(
            f"Inicio: {bloque['inicio']} KB | "
            f"Tamaño: {bloque['tamano']} KB | "
            f"Estado: {estado}"
        )

    print("-" * 45)


# 1. Asignar tres procesos
print("\n1. ASIGNANDO PROCESOS")

print(simulador.asignar_proceso("P1", 200, "first_fit"))
print(simulador.asignar_proceso("P2", 300, "first_fit"))
print(simulador.asignar_proceso("P3", 150, "first_fit"))

mostrar_memoria()


# 2. Liberar el proceso P2
print("\n2. LIBERANDO P2")

print(simulador.liberar_proceso("P2"))

mostrar_memoria()


# 3. Liberar P1 y comprobar la unión de bloques
print("\n3. LIBERANDO P1")

print(simulador.liberar_proceso("P1"))

mostrar_memoria()