function TablaProcesos({ memoria, onLiberarProceso, cargando }) {
  const procesos = memoria.filter((bloque) => bloque.proceso !== null);

  return (
    <div className="tabla-container">
      <h2>Procesos en memoria</h2>

      {procesos.length === 0 ? (
        <p className="mensaje-vacio">No hay procesos asignados actualmente.</p>
      ) : (
        <div className="tabla-scroll">
          <table>
            <thead>
              <tr>
                <th>Proceso</th>
                <th>Inicio</th>
                <th>Tamaño</th>
                <th>Acción</th>
              </tr>
            </thead>

            <tbody>
              {procesos.map((proceso) => (
                <tr key={proceso.proceso}>
                  <td>
                    <strong>{proceso.proceso}</strong>
                  </td>

                  <td>{proceso.inicio} KB</td>

                  <td>{proceso.tamano} KB</td>

                  <td>
                    <button
                      className="btn-liberar"
                      onClick={() => onLiberarProceso(proceso.proceso)}
                      disabled={cargando}
                    >
                      Liberar
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default TablaProcesos;
