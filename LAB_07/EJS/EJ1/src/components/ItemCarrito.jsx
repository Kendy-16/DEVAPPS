function ItemCarrito({ producto, onEliminar }) {
  return (
    <article className="item-carrito">
      <img
        src={producto.image}
        alt={producto.title}
      />

      <div className="item-info">
        <h3>{producto.title}</h3>

        <span>
          {producto.category}
        </span>
      </div>

      <strong className="item-precio">
        ${producto.price.toFixed(2)}
      </strong>

      <button
        className="btn-eliminar"
        onClick={() => onEliminar(producto.id)}
      >
        Eliminar
      </button>
    </article>
  );
}

export default ItemCarrito;