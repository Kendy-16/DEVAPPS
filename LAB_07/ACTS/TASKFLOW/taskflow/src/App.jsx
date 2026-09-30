import { 
  BrowserRouter,
  Routes,
  Route,
  Link,
} from "react-router-dom";

import Inicio from "./pages/Inicio";
import TareasLayout from "./pages/TareasLayout";
import TareasLista from "./pages/TareasLista";
import TareaDetalle from "./pages/TareaDetalle";

import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <div className="app">

        <header className="header">
          <div className="header-contenido">
            <div>
              <h1>TaskFlow</h1>
              <p>Organiza tus tareas de manera sencilla</p>
            </div>

            <nav className="navegacion">
              <Link to="/">Inicio</Link>
              <Link to="/tareas">Mis tareas</Link>
            </nav>
          </div>
        </header>

        <main className="contenido">
          <Routes>

            <Route
              path="/"
              element={<Inicio />}
            />

            <Route
              path="/tareas"
              element={<TareasLayout />}
            >
              <Route
                index
                element={<TareasLista />}
              />

              <Route
                path=":id"
                element={<TareaDetalle />}
              />
            </Route>

            <Route
              path="*"
              element={
                <div className="pagina-error">
                  <h2>Página no encontrada</h2>
                  <Link to="/">Volver al inicio</Link>
                </div>
              }
            />

          </Routes>
        </main>

        <footer className="footer">
          <p>TaskFlow © 2026</p>
        </footer>

      </div>
    </BrowserRouter>
  );
}

export default App;