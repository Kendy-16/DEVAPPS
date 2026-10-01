import {
  Link,
  NavLink,
  Outlet
} from "react-router-dom";

function CatalogoLayout({ cantidad }) {
  return (
    <div className="app-contenedor">

      <header className="navbar">
        <Link to="/catalogo" className="logo">
          <span>SHOP</span>
          <small>React Store</small>
        </Link>

        <nav>
          <NavLink
            to="/catalogo"
            end
          >
            Catálogo
          </NavLink>

          <NavLink to="/catalogo/carrito">
            🛒 Carrito
            <span className="badge">
              {cantidad}
            </span>
          </NavLink>
        </nav>
      </header>

      <Outlet />

      <footer className="footer">
        <p>
          React Store · Catálogo de productos
        </p>
      </footer>

    </div>
  );
}

export default CatalogoLayout;