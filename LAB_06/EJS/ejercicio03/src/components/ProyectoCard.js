function ProyectoCard({ proyecto, onCambiarEstado, onEliminar }) {
  const claseEstado = proyecto.estado.toLowerCase().replace(" ", "-");

  return (
    <article className="project-card">
      <div className="card-top">
        <span className="project-id">PROYECTO #{proyecto.id}</span>
        <span className={`status-badge estado-${claseEstado}`}>
          <span className="status-dot" />
          {proyecto.estado}
        </span>
      </div>

      <div className="card-body">
        <div className="project-icon" aria-hidden="true">◇</div>
        <h2>{proyecto.nombre}</h2>
        <p>{proyecto.descripcion}</p>
      </div>

      <div className="card-actions">
        <button
          type="button"
          className="advance-button"
          onClick={() => onCambiarEstado(proyecto.id)}
        >
          {proyecto.estado === "Finalizado" ? "Reiniciar estado" : "Avanzar estado"}
          <span aria-hidden="true">→</span>
        </button>

        <button
          type="button"
          className="delete-button"
          onClick={() => onEliminar(proyecto.id)}
        >
          Eliminar
        </button>
      </div>
    </article>
  );
}

export default ProyectoCard;