from services.simulador import SimuladorMemoria
from utils.metricas import calcular_metricas


simulador = SimuladorMemoria(1024)

# Asignar procesos
simulador.asignar_proceso("P1", 200, "first_fit")
simulador.asignar_proceso("P2", 300, "first_fit")
simulador.asignar_proceso("P3", 150, "first_fit")

# Liberar P2 para generar dos bloques libres separados
simulador.liberar_proceso("P2")

# Calcular métricas
metricas = calcular_metricas(
    simulador.obtener_memoria(),
    simulador.memoria_total
)

print("\n========== MÉTRICAS DE MEMORIA ==========")

for indicador, valor in metricas.items():
    print(f"{indicador}: {valor}")