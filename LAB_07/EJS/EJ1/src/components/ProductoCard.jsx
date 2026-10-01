function ProductoCard({ producto, onAgregar }) {
  return (
    <article className="producto-card">
      <div className="producto-imagen">
        <img src={producto.image} alt={producto.title} />
      </div>

      <div className="producto-info">
        <span className="producto-categoria">
          {producto.category}
        </span>

        <h3>{producto.title}</h3>

        <div className="producto-footer">
          <span className="precio">
            ${producto.price.toFixed(2)}
          </span>

          <button
            className="btn-agregar"
            onClick={() => onAgregar(producto)}
          >
            + Agregar
          </button>
        </div>
      </div>
    </article>
  );
}

export default ProductoCard;