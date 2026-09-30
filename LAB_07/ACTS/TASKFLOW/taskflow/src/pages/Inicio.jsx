import { Link } from "react-router-dom";

function Inicio() {
  return (
    <section className="inicio">

      <h2>Bienvenido a TaskFlow</h2>

      <p>
        Organiza, consulta y administra tus tareas
        de manera sencilla.
      </p>

      <Link
        to="/tareas"
        className="boton-principal"
      >
        Ver mis tareas
      </Link>

    </section>
  );
}

export default Inicio;