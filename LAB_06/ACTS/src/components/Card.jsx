function Card({
  nombre,
  descripcion,
  categoria,
  seleccionada,
  onSeleccionar
}) {
  return (
    <div
      className="card"
      onClick={onSeleccionar}
      style={{
        border: seleccionada ? "3px solid blue" : "1px solid #ccc",
        padding: "20px",
        margin: "10px",
        cursor: "pointer"
      }}
    >
      <h2>{nombre}</h2>

      <p>{descripcion}</p>

      <p>
        <strong>Categoría:</strong> {categoria}
      </p>

      <p>
        <strong>Estado:</strong>{" "}
        {seleccionada ? "Seleccionada" : "No seleccionada"}
      </p>
    </div>
  );
}

export default Card;