import { useState } from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import CatalogoLayout from "./pages/CatalogoLayout";
import Catalogo from "./pages/Catalogo";
import Carrito from "./components/Carrito";

function App() {
  const [carrito, setCarrito] = useState([]);

  const agregarAlCarrito = (producto) => {
    setCarrito((carritoActual) => {
      const existe = carritoActual.some(
        (item) => item.id === producto.id
      );

      if (existe) {
        return carritoActual;
      }

      return [...carritoActual, producto];
    });
  };

  const eliminarDelCarrito = (id) => {
    setCarrito((carritoActual) =>
      carritoActual.filter(
        (producto) => producto.id !== id
      )
    );
  };

  return (
    <BrowserRouter>
      <Routes>

        <Route
          path="/"
          element={
            <Navigate to="/catalogo" replace />
          }
        />

        <Route
          path="/catalogo"
          element={
            <CatalogoLayout
              cantidad={carrito.length}
            />
          }
        >
          <Route
            index
            element={
              <Catalogo
                onAgregar={agregarAlCarrito}
              />
            }
          />

          <Route
            path="carrito"
            element={
              <Carrito
                carrito={carrito}
                onEliminar={eliminarDelCarrito}
              />
            }
          />
        </Route>

        <Route
          path="*"
          element={
            <Navigate to="/catalogo" replace />
          }
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;