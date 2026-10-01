function BuscadorProducto({ value, onChange }) {
  const manejarEnvio = (evento) => {
    evento.preventDefault();
  };

  return (
    <form className="buscador" onSubmit={manejarEnvio}>
      <span className="buscador-icono">⌕</span>

      <input
        type="text"
        placeholder="Buscar productos por nombre..."
        value={value}
        onChange={(evento) => onChange(evento.target.value)}
      />

      {value && (
        <button
          type="button"
          className="btn-limpiar"
          onClick={() => onChange("")}
        >
          ×
        </button>
      )}
    </form>
  );
}

export default BuscadorProducto;