import { useState } from "react";

const camposVacios = {
  nombre: "",
  correo: "",
  ciudad: "",
};

function FormularioRegistro({ onRegistrar }) {
  const [campos, setCampos] = useState(camposVacios);

  function manejarCambio(event) {
    const { name, value } = event.target;

    setCampos((anteriores) => ({
      ...anteriores,
      [name]: value,
    }));
  }

  function manejarEnvio(event) {
    event.preventDefault();

    onRegistrar({
      nombre: campos.nombre.trim(),
      correo: campos.correo.trim(),
      ciudad: campos.ciudad.trim(),
    });

    setCampos(camposVacios);
  }

  return (
    <section className="panel">
      <div className="panel-heading">
        <span className="panel-icon">✦</span>
        <div>
          <span className="section-label">NUEVO REGISTRO</span>
          <h2>Ingresa tus datos</h2>
        </div>
      </div>

      <form onSubmit={manejarEnvio} className="registro-form">
        <label htmlFor="nombre">Nombre completo</label>
        <input
          id="nombre"
          name="nombre"
          type="text"
          placeholder="Ejemplo: Ana Torres"
          value={campos.nombre}
          onChange={manejarCambio}
          required
        />

        <label htmlFor="correo">Correo electrónico</label>
        <input
          id="correo"
          name="correo"
          type="email"
          placeholder="ana@ejemplo.com"
          value={campos.correo}
          onChange={manejarCambio}
          required
        />

        <label htmlFor="ciudad">Ciudad</label>
        <input
          id="ciudad"
          name="ciudad"
          type="text"
          placeholder="Ejemplo: Arequipa"
          value={campos.ciudad}
          onChange={manejarCambio}
          required
        />

        <button type="submit" className="primary-button">
          Registrar información <span aria-hidden="true">→</span>
        </button>
      </form>
    </section>
  );
}

export default FormularioRegistro;