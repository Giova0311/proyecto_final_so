const API_URL = "http://127.0.0.1:5000/api";

async function manejarRespuesta(respuesta) {
  const datos = await respuesta.json();

  if (!respuesta.ok) {
    throw new Error(datos.error || "Error en la comunicación con el servidor.");
  }

  return datos;
}

// Consultar memoria y métricas
export async function obtenerMemoria() {
  const respuesta = await fetch(`${API_URL}/memoria`);
  return manejarRespuesta(respuesta);
}

// Crear un proceso
export async function crearProceso(proceso) {
  const respuesta = await fetch(`${API_URL}/procesos`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(proceso),
  });

  return manejarRespuesta(respuesta);
}

// Liberar un proceso
export async function liberarProceso(procesoId) {
  const respuesta = await fetch(
    `${API_URL}/procesos/${encodeURIComponent(procesoId)}`,
    {
      method: "DELETE",
    },
  );

  return manejarRespuesta(respuesta);
}

// Reiniciar la memoria
export async function reiniciarMemoria(memoriaTotal = 1024) {
  const respuesta = await fetch(`${API_URL}/memoria/reiniciar`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      memoria_total: memoriaTotal,
    }),
  });

  return manejarRespuesta(respuesta);
}

export async function compararAlgoritmos() {
  const respuesta = await fetch(`${API_URL}/comparacion`, {
    method: "POST",
  });

  return manejarRespuesta(respuesta);
}
