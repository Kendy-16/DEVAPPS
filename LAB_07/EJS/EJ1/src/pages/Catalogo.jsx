import { useEffect, useState } from "react";
import ListaProductos from "../components/ListaProductos";
import BuscadorProducto from "../components/BuscadorProducto";

function Catalogo({ onAgregar }) {
  const [productos, setProductos] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");
  const [busqueda, setBusqueda] = useState("");

  useEffect(() => {
    fetch("https://fakestoreapi.com/products")
      .then((respuesta) => {
        if (!respuesta.ok) {
          throw new Error(
            "No se pudieron cargar los productos."
          );
        }

        return respuesta.json();
      })
      .then((datos) => {
        setProductos(datos);
      })
      .catch((err) => {
        setError(err.message);
      })
      .finally(() => {
        setCargando(false);
      });
  }, []);

  const productosFiltrados = productos.filter((producto) =>
    producto.title
      .toLowerCase()
      .includes(busqueda.toLowerCase())
  );

  if (cargando) {
    return (
      <main className="estado">
        <div className="spinner"></div>
        <h2>Cargando catálogo...</h2>
        <p>Estamos obteniendo los productos.</p>
      </main>
    );
  }

  if (error) {
    return (
      <main className="estado error">
        <div className="estado-icono">⚠</div>
        <h2>Ocurrió un problema</h2>
        <p>{error}</p>
      </main>
    );
  }

  return (
    <main className="catalogo">
      <section className="hero">
        <div>
          <span className="etiqueta">
            TIENDA ONLINE
          </span>

          <h1>
            Encuentra tu
            <br />
            próximo favorito.
          </h1>

          <p>
            Explora nuestro catálogo y agrega tus
            productos favoritos al carrito.
          </p>
        </div>
      </section>

      <section className="catalogo-seccion">
        <div className="catalogo-header">
          <div>
            <span className="etiqueta">CATÁLOGO</span>

            <h2>
              Todos los productos
            </h2>
          </div>

          <span className="contador-productos">
            {productosFiltrados.length} productos
          </span>
        </div>

        <BuscadorProducto
          value={busqueda}
          onChange={setBusqueda}
        />

        <ListaProductos
          productos={productosFiltrados}
          onAgregar={onAgregar}
        />
      </section>
    </main>
  );
}

export default Catalogo;