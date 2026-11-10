function BarraMemoria({ memoria, memoriaTotal }) {
  const colores = [
    "#2878D0",
    "#16A078",
    "#D69A35",
    "#8957C5",
    "#D65D78",
    "#258EAA",
  ];

  // Obtener los procesos únicos
  const procesos = [
    ...new Set(
      memoria
        .filter((bloque) => bloque.proceso !== null)
        .map((bloque) => bloque.proceso),
    ),
  ];

  return (
    <div className="barra-memoria-container">
      <div className="barra-memoria">
        {memoria.map((bloque, indice) => {
          const porcentaje = (bloque.tamano / memoriaTotal) * 100;

          const color = bloque.proceso
            ? colores[procesos.indexOf(bloque.proceso) % colores.length]
            : "#A1A1AA";

          return (
            <div
              key={`${bloque.inicio}-${indice}`}
              className="bloque-memoria"
              style={{
                width: `${porcentaje}%`,
                backgroundColor: color,
              }}
              title={`${bloque.proceso || "Libre"}: ${bloque.tamano} KB`}
            >
              <span>{bloque.proceso || "Libre"}</span>

              <small>{bloque.tamano} KB</small>
            </div>
          );
        })}
      </div>

      <div className="barra-leyenda">
        <span>Memoria total: {memoriaTotal} KB</span>

        <span>{memoria.length} bloques</span>
      </div>
    </div>
  );
}

export default BarraMemoria;
