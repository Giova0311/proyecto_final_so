import React, { useEffect, useState } from "react";
import Comparacion from "./components/Comparacion";
import BarraMemoria from "./components/BarraMemoria";
import FormularioProceso from "./components/FormularioProceso";
import TablaProcesos from "./components/TablaProcesos";
import Estadisticas from "./components/Estadisticas";

import {
  obtenerMemoria,
  crearProceso,
  liberarProceso,
  reiniciarMemoria,
} from "./services/api";

import "./App.css";

function App() {
  const [memoria, setMemoria] = useState([]);
  const [metricas, setMetricas] = useState(null);

  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState("");
  const [mensaje, setMensaje] = useState("");

  // Actualizar los datos recibidos desde Flask
  const actualizarEstado = (datos) => {
    setMemoria(datos.memoria);
    setMetricas(datos.metricas);
  };

  // Consultar memoria al iniciar la aplicación
  useEffect(() => {
    const cargarDatos = async () => {
      try {
        setCargando(true);

        const datos = await obtenerMemoria();

        actualizarEstado(datos);
      } catch (err) {
        setError(err.message);
      } finally {
        setCargando(false);
      }
    };

    cargarDatos();
  }, []);

  // Crear un proceso
  const manejarCrearProceso = async (proceso) => {
    try {
      setCargando(true);
      setError("");
      setMensaje("");

      const datos = await crearProceso(proceso);

      actualizarEstado(datos);
      setMensaje(datos.mensaje);
    } catch (err) {
      setError(err.message);
    } finally {
      setCargando(false);
    }
  };

  // Liberar un proceso
  const manejarLiberarProceso = async (procesoId) => {
    try {
      setCargando(true);
      setError("");
      setMensaje("");

      const datos = await liberarProceso(procesoId);

      actualizarEstado(datos);
      setMensaje(datos.mensaje);
    } catch (err) {
      setError(err.message);
    } finally {
      setCargando(false);
    }
  };

  // Reiniciar la simulación
  const manejarReinicio = async () => {
    const confirmar = window.confirm(
      "¿Estás seguro de que deseas reiniciar la memoria? Se eliminarán todos los procesos.",
    );

    if (!confirmar) return;

    try {
      setCargando(true);
      setError("");
      setMensaje("");

      const datos = await reiniciarMemoria(1024);

      actualizarEstado(datos);
      setMensaje(datos.mensaje);
    } catch (err) {
      setError(err.message);
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="aplicacion">
      <header className="encabezado">
        <div>
          <h1>Simulador de Gestión de Memoria RAM</h1>

          <p>
            Sistema de asignación y administración de memoria mediante
            algoritmos First Fit y Best Fit.
          </p>
        </div>

        <button
          className="btn-reiniciar"
          onClick={manejarReinicio}
          disabled={cargando}
        >
          Reiniciar simulación
        </button>
      </header>

      {error && <div className="alerta alerta-error">{error}</div>}

      {mensaje && <div className="alerta alerta-exito">{mensaje}</div>}

      {cargando && memoria.length === 0 ? (
        <p className="estado-carga">Conectando con el servidor...</p>
      ) : metricas ? (
        <main className="contenido">
          <section className="seccion-memoria">
            <h2>Visualización de memoria</h2>

            <BarraMemoria
              memoria={memoria}
              memoriaTotal={metricas.memoria_total}
            />
          </section>

          <section className="seccion-estadisticas">
            <Estadisticas metricas={metricas} />
          </section>

          <div className="seccion-inferior">
            <FormularioProceso
              onCrearProceso={manejarCrearProceso}
              cargando={cargando}
            />

            <TablaProcesos
              memoria={memoria}
              onLiberarProceso={manejarLiberarProceso}
              cargando={cargando}
            />
          </div>
        </main>
      ) : (
        !error && <p className="estado-carga">Cargando simulador...</p>
      )}

      <Comparacion />

      <footer className="pie-pagina">
        Proyecto Final - Sistemas Operativos
      </footer>
    </div>
  );
}

export default App;
