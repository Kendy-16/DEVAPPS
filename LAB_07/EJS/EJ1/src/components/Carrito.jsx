import { Link } from "react-router-dom";
import ItemCarrito from "./ItemCarrito";

function Carrito({ carrito, onEliminar }) {
  const total = carrito.reduce(
    (acumulado, producto) => acumulado + producto.price,
    0
  );

  if (carrito.length === 0) {
    return (
      <main className="carrito-vacio">
        <div className="icono-carrito">🛒</div>

        <h1>Tu carrito está vacío</h1>

        <p>
          Agrega algunos productos desde el catálogo.
        </p>

        <Link to="/catalogo" className="btn-volver">
          Ir al catálogo
        </Link>
      </main>
    );
  }

  return (
    <main className="carrito">
      <div className="titulo-seccion">
        <div>
          <span className="etiqueta">COMPRA</span>
          <h1>Mi carrito</h1>
        </div>

        <span className="cantidad-carrito">
          {carrito.length} producto(s)
        </span>
      </div>

      <div className="carrito-contenido">
        <section className="items-carrito">
          {carrito.map((producto) => (
            <ItemCarrito
              key={producto.id}
              producto={producto}
              onEliminar={onEliminar}
            />
          ))}
        </section>

        <aside className="resumen">
          <h2>Resumen</h2>

          <div className="resumen-linea">
            <span>Productos</span>
            <span>{carrito.length}</span>
          </div>

          <div className="resumen-total">
            <span>Total</span>
            <strong>${total.toFixed(2)}</strong>
          </div>

          <button className="btn-comprar">
            Finalizar compra
          </button>
        </aside>
      </div>
    </main>
  );
}

export default Carrito;