import { useDispatch, useSelector } from "react-redux";
import { eliminarGasto } from "../store/acciones.js";

const formatoSoles = new Intl.NumberFormat("es-PE", {
  style: "currency",
  currency: "PEN",
});

function ListaGastos() {
  const gastos = useSelector((estado) => estado.gastos);
  const dispatch = useDispatch();

  return (
    <section className="panel historial-panel">
      <div className="panel-encabezado">
        <span className="numero-seccion">02 / MOVIMIENTOS</span>
        <h2>Historial</h2>
        <p>Consulta y administra los gastos registrados.</p>
      </div>

      {gastos.length === 0 ? (
        <div className="estado-vacio">
          <span className="estado-vacio-icono">☀</span>
          <h3>Aún no hay gastos</h3>
          <p>Agrega tu primer gasto para verlo aquí.</p>
        </div>
      ) : (
        <ul className="lista-gastos">
          {gastos.map((gasto) => (
            <li className="gasto" key={gasto.id}>
              <div className="gasto-icono" aria-hidden="true">
                {gasto.categoria === "Alimentación"
                  ? "◒"
                  : gasto.categoria === "Transporte"
                  ? "↗"
                  : gasto.categoria === "Estudios"
                  ? "✎"
                  : gasto.categoria === "Salud"
                  ? "✳"
                  : "●"}
              </div>

              <div className="gasto-info">
                <strong>{gasto.descripcion}</strong>
                <span>
                  {gasto.categoria} ·{" "}
                  {new Date(gasto.fecha).toLocaleDateString(
                    "es-PE"
                  )}
                </span>
              </div>

              <strong className="gasto-monto">
                −{formatoSoles.format(gasto.monto)}
              </strong>

              <button
                className="boton-eliminar"
                type="button"
                aria-label={`Eliminar ${gasto.descripcion}`}
                onClick={() =>
                  dispatch(eliminarGasto(gasto.id))
                }
              >
                ×
              </button>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

export default ListaGastos;