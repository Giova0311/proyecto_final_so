import React, { useState } from "react";
import { compararAlgoritmos } from "../services/api";

function Comparacion() {
  const [resultados, setResultados] = useState([]);
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState("");

  const ejecutarComparacion = async () => {
    setCargando(true);
    setError("");

    try {
      const datos = await compararAlgoritmos();
      setResultados(datos.resultados);
    } catch (error) {
      setError(error.message);
    } finally {
      setCargando(false);
    }
  };

  return (
    <section className="seccion">
      <h2>Comparación de algoritmos</h2>

      <p>
        Ejecuta los tres escenarios para comparar el comportamiento de First Fit
        y Best Fit.
      </p>

      <button
        className="boton-comparar"
        onClick={ejecutarComparacion}
        disabled={cargando}
      >
        {cargando ? "Ejecutando experimentos..." : "Ejecutar comparación"}
      </button>

      {error && <div className="mensaje-error">{error}</div>}

      {resultados.map((escenario, indice) => (
        <div className="resultado-escenario" key={indice}>
          <h3>{escenario.escenario}</h3>

          <table className="tabla-comparacion">
            <thead>
              <tr>
                <th>Métrica</th>
                <th>First Fit</th>
                <th>Best Fit</th>
              </tr>
            </thead>

            <tbody>
              <tr>
                <td>Procesos asignados</td>
                <td>{escenario.first_fit.asignados}</td>
                <td>{escenario.best_fit.asignados}</td>
              </tr>

              <tr>
                <td>Procesos rechazados</td>
                <td>{escenario.first_fit.rechazados}</td>
                <td>{escenario.best_fit.rechazados}</td>
              </tr>

              <tr>
                <td>Utilización</td>
                <td>{escenario.first_fit.utilizacion}%</td>
                <td>{escenario.best_fit.utilizacion}%</td>
              </tr>

              <tr>
                <td>Fragmentación externa</td>
                <td>{escenario.first_fit.fragmentacion}%</td>
                <td>{escenario.best_fit.fragmentacion}%</td>
              </tr>

              <tr>
                <td>Mayor bloque libre</td>
                <td>{escenario.first_fit.bloque_libre_mayor} KB</td>
                <td>{escenario.best_fit.bloque_libre_mayor} KB</td>
              </tr>
            </tbody>
          </table>
        </div>
      ))}
    </section>
  );
}

export default Comparacion;
