import { Link, useParams } from "react-router-dom";

function TareaDetalle() {
  const { id } = useParams();

  return (
    <div className="detalle">

      <h2>Detalle de la tarea</h2>

      <p className="detalle-id">
        ID de la tarea: <strong>{id}</strong>
      </p>

      <Link
        to="/tareas"
        className="boton-principal"
      >
        ← Volver a mis tareas
      </Link>

    </div>
  );
}

export default TareaDetalle;