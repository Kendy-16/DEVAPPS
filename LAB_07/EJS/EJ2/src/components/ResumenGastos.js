import { useSelector } from "react-redux";

const formatoSoles = new Intl.NumberFormat("es-PE", {
  style: "currency",
  currency: "PEN",
});

function ResumenGastos() {
  const gastos = useSelector((estado) => estado.gastos);

  // El total se calcula a partir de los gastos.
  // No se guarda como otro estado.
  const total = gastos.reduce(
    (acumulado, gasto) => acumulado + gasto.monto,
    0
  );

  const categorias = [
    "Alimentación",
    "Transporte",
    "Estudios",
    "Salud",
    "Otros",
  ];

  return (
    <section className="resumen" aria-label="Resumen de gastos">
      <div className="resumen-decoracion">✳</div>

      <span className="resumen-etiqueta">TU BALANCE DE GASTOS</span>
      <h2>{formatoSoles.format(total)}</h2>
      <p>Total acumulado</p>

      <div className="resumen-divider" />

      <div className="resumen-datos">
        <div>
          <strong>{gastos.length}</strong>
          <span>
            {gastos.length === 1
              ? "gasto registrado"
              : "gastos registrados"}
          </span>
        </div>

        <div>
          <strong>
            {
              categorias.filter((categoria) =>
                gastos.some(
                  (gasto) => gasto.categoria === categoria
                )
              ).length
            }
          </strong>
          <span>categorías usadas</span>
        </div>
      </div>
    </section>
  );
}

export default ResumenGastos;