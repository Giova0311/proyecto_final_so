import React from "react";
function FormularioProceso({ onCrearProceso, cargando }) {
  const [procesoId, setProcesoId] = React.useState("");
  const [tamano, setTamano] = React.useState("");
  const [algoritmo, setAlgoritmo] = React.useState("first_fit");

  const manejarEnvio = (e) => {
    e.preventDefault();

    onCrearProceso({
      proceso_id: procesoId.trim(),
      tamano: Number(tamano),
      algoritmo: algoritmo,
    });

    setProcesoId("");
    setTamano("");
  };

  return (
    <div className="formulario-container">
      <h2>Crear nuevo proceso</h2>

      <form onSubmit={manejarEnvio}>
        <div className="campo">
          <label>Identificador del proceso</label>

          <input
            type="text"
            placeholder="Ejemplo: P1"
            value={procesoId}
            onChange={(e) => setProcesoId(e.target.value)}
            required
          />
        </div>

        <div className="campo">
          <label>Tamaño del proceso (KB)</label>

          <input
            type="number"
            placeholder="Ejemplo: 200"
            value={tamano}
            onChange={(e) => setTamano(e.target.value)}
            min="1"
            step="1"
            required
          />
        </div>

        <div className="campo">
          <label>Algoritmo de asignación</label>

          <select
            value={algoritmo}
            onChange={(e) => setAlgoritmo(e.target.value)}
          >
            <option value="first_fit">First Fit</option>
            <option value="best_fit">Best Fit</option>
          </select>
        </div>

        <button type="submit" disabled={cargando}>
          {cargando ? "Procesando..." : "Asignar proceso"}
        </button>
      </form>
    </div>
  );
}

export default FormularioProceso;
