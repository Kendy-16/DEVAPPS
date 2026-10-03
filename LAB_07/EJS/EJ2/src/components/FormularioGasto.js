import { useState } from "react";
import { useDispatch } from "react-redux";
import { agregarGasto } from "../store/acciones.js";

function FormularioGasto() {
  const dispatch = useDispatch();

  const [descripcion, setDescripcion] = useState("");
  const [monto, setMonto] = useState("");
  const [categoria, setCategoria] = useState("Alimentación");
  const [error, setError] = useState("");

  const manejarEnvio = (evento) => {
    evento.preventDefault();

    const descripcionLimpia = descripcion.trim();
    const montoNumerico = Number(monto);

    if (!descripcionLimpia) {
      setError("Escribe una descripción para el gasto.");
      return;
    }

    if (!Number.isFinite(montoNumerico) || montoNumerico <= 0) {
      setError("Ingresa un monto mayor que cero.");
      return;
    }

    dispatch(
      agregarGasto({
        id: crypto.randomUUID(),
        descripcion: descripcionLimpia,
        monto: montoNumerico,
        categoria,
        fecha: new Date().toISOString(),
      })
    );

    setDescripcion("");
    setMonto("");
    setCategoria("Alimentación");
    setError("");
  };

  return (
    <section className="panel formulario-panel">
      <div className="panel-encabezado">
        <span className="numero-seccion">01 / REGISTRO</span>
        <h2>Nuevo gasto</h2>
        <p>Anota tus movimientos para saber en qué se va tu dinero.</p>
      </div>

      <form onSubmit={manejarEnvio}>
        <label htmlFor="descripcion">Descripción</label>
        <input
          id="descripcion"
          type="text"
          value={descripcion}
          onChange={(evento) =>
            setDescripcion(evento.target.value)
          }
          placeholder="Ejemplo: Almuerzo en la universidad"
          maxLength={100}
        />

        <div className="formulario-fila">
          <div className="campo">
            <label htmlFor="monto">Monto (S/)</label>
            <input
              id="monto"
              type="number"
              min="0.01"
              step="0.01"
              value={monto}
              onChange={(evento) =>
                setMonto(evento.target.value)
              }
              placeholder="0.00"
            />
          </div>

          <div className="campo">
            <label htmlFor="categoria">Categoría</label>
            <select
              id="categoria"
              value={categoria}
              onChange={(evento) =>
                setCategoria(evento.target.value)
              }
            >
              <option>Alimentación</option>
              <option>Transporte</option>
              <option>Estudios</option>
              <option>Salud</option>
              <option>Otros</option>
            </select>
          </div>
        </div>

        {error && (
          <p className="mensaje-error" role="alert">
            {error}
          </p>
        )}

        <button className="boton-agregar" type="submit">
          <span>＋</span> Agregar gasto
        </button>
      </form>
    </section>
  );
}

export default FormularioGasto;