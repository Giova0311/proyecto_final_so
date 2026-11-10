# Simulador de Gestión de Memoria RAM (asignación contigua)

Proyecto final – Sistemas Operativos (UCC, periodo 2610) · Opción 2: Gestión de memoria.

Simulador educativo que representa la memoria como bloques libres y ocupados,
permite asignar y liberar procesos, y compara las estrategias **First Fit** y
**Best Fit** mediante métricas de utilización y fragmentación externa.
No administra la RAM física del equipo: opera sobre una memoria hipotética de 1024 KB.

## Estructura

```
Proyecto_final_so/
├── backend/                  API Flask + lógica del simulador
│   ├── app.py                Punto de entrada (puerto 5000)
│   ├── routes/               Endpoints REST
│   ├── services/             algoritmos.py (First/Best Fit) y simulador.py
│   ├── utils/metricas.py     Cálculo de métricas
│   ├── tests/                Escenarios y pruebas reproducibles
│   └── requirements.txt
├── frontend/                 Interfaz React
├── evidencias/               Resultados de los escenarios (salida de los scripts)
├── informe/                  Informe técnico (PDF y Word)
└── README.md
```

## Requisitos

- Python 3.11 o superior
- Node.js y npm (compatible con Create React App 5 / React 19)

## 1. Ejecutar el backend

Desde la carpeta `backend/`:

```bash
python -m venv venv

# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
python app.py
```

La API queda en `http://127.0.0.1:5000`.

| Método | Ruta | Función |
|---|---|---|
| GET | `/api/memoria` | Estado de la memoria y métricas |
| POST | `/api/procesos` | Asignar proceso `{proceso_id, tamano, algoritmo}` |
| DELETE | `/api/procesos/<id>` | Liberar proceso |
| POST | `/api/memoria/reiniciar` | Reiniciar la simulación |
| POST | `/api/comparacion` | Ejecutar los escenarios 1 a 3 con ambos algoritmos |

`algoritmo` acepta `first_fit` o `best_fit`.

## 2. Ejecutar el frontend

En otra terminal, desde `frontend/`:

```bash
npm install
npm start
```

Abre `http://localhost:3000` (el backend debe estar corriendo).

## 3. Reproducir los experimentos (sin interfaz)

Desde la carpeta `backend/` (con el entorno virtual activo):

```bash
# Escenarios 1 a 3 (distribuciones iniciales fijas) – comparación consolidada
python -m tests.comparacion_general

# Escenario 4 (secuencia larga de asignar/liberar, 20 semillas fijas)
python -m tests.escenario_4_secuencia_larga

# Pruebas individuales
python -m tests.prueba_escenario_2
python -m tests.prueba_escenario_3
python -m tests.prueba_comparacion
python -m tests.prueba_simulador     # asignación, liberación y unión de bloques
python -m tests.prueba_metricas
```

> Importante: ejecutar con `python -m tests.<nombre>` **desde `backend/`**.
> Si se ejecuta `python tests/<nombre>.py`, Python no encuentra el paquete `services`.

Los resultados de los escenarios se guardan en `evidencias/`.

## Escenarios

| # | Descripción | Qué evidencia |
|---|---|---|
| 1 | Memoria fragmentada, 1 solicitud de 250 KB | Misma utilización; Best Fit deja menos fragmentación |
| 2 | Memoria fragmentada, 3 solicitudes (90, 115, 190 KB) | Best Fit atiende las 3; First Fit rechaza una |
| 3 | Memoria fragmentada, 1 solicitud de 250 KB | Ambos rechazan: 450 KB libres, pero el mayor bloque es de 200 KB |
| 4 | 300 operaciones pseudoaleatorias (asignar/liberar), 20 semillas | Comparación sobre muchas secuencias, con fragmentación generada por el propio uso |

## Métricas

- **Utilización** = memoria ocupada / memoria total × 100
- **Fragmentación externa** = (memoria libre − mayor bloque libre) / memoria libre × 100
  (indicador operativo del proyecto; existen otras formas de medirla)
- Procesos asignados / rechazados, cantidad de bloques libres y tamaño del mayor bloque libre.

## Limitaciones

Modelo simplificado: sin paginación, segmentación, swapping ni protección de memoria.
El estado vive en la memoria del proceso Flask y se pierde al reiniciar el servidor.
Los resultados aplican a los escenarios probados y no deben generalizarse.
