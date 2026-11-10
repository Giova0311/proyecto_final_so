function Estadisticas({ metricas }) {
  const indicadores = [
    {
      titulo: "Memoria total",
      valor: `${metricas.memoria_total} KB`,
    },
    {
      titulo: "Memoria ocupada",
      valor: `${metricas.memoria_ocupada} KB`,
    },
    {
      titulo: "Memoria libre",
      valor: `${metricas.memoria_libre} KB`,
    },
    {
      titulo: "Utilización",
      valor: `${metricas.porcentaje_uso}%`,
    },
    {
      titulo: "Bloques libres",
      valor: metricas.cantidad_bloques_libres,
    },
    {
      titulo: "Bloque libre mayor",
      valor: `${metricas.bloque_libre_mayor} KB`,
    },
    {
      titulo: "Fragmentación externa",
      valor: `${metricas.fragmentacion_externa}%`,
    },
  ];

  return (
    <div className="estadisticas-container">
      <h2>Estadísticas de memoria</h2>

      <div className="estadisticas-grid">
        {indicadores.map((indicador, index) => (
          <div className="estadistica-card" key={index}>
            <span>{indicador.titulo}</span>
            <strong>{indicador.valor}</strong>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Estadisticas;
