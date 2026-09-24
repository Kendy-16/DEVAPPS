import { useState } from "react";

function Formulario({ onAgregar }) {

  const [nombre, setNombre] = useState("");
  const [descripcion, setDescripcion] = useState("");

  function manejarEnvio(event) {
    event.preventDefault();

    if (nombre.trim() === "" || descripcion.trim() === "") {
      return;
    }

    onAgregar({
      nombre: nombre,
      descripcion: descripcion
    });

    setNombre("");
    setDescripcion("");
  }

  return (
    <form onSubmit={manejarEnvio}>

      <h2>Agregar nueva tarjeta</h2>

      <div>
        <label>Nombre:</label>
        <input
          type="text"
          value={nombre}
          onChange={(event) => setNombre(event.target.value)}
          placeholder="Ingrese un nombre"
        />
      </div>

      <div>
        <label>Descripción:</label>
        <input
          type="text"
          value={descripcion}
          onChange={(event) => setDescripcion(event.target.value)}
          placeholder="Ingrese una descripción"
        />
      </div>

      <button type="submit">
        Agregar
      </button>

    </form>
  );
}

export default Formulario;