import ProductoCard from "./ProductoCard";

function ListaProductos({ productos, onAgregar }) {
  if (productos.length === 0) {
    return (
      <div className="sin-resultados">
        <p>No se encontraron productos.</p>
      </div>
    );
  }

  return (
    <div className="lista-productos">
      {productos.map((producto) => (
        <ProductoCard
          key={producto.id}
          producto={producto}
          onAgregar={onAgregar}
        />
      ))}
    </div>
  );
}

export default ListaProductos;