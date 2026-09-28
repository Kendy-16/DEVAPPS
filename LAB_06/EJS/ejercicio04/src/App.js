import DirectorioUsuarios from "./components/DirectorioUsuarios";
import "./App.css";

function App() {
  return (
    <div className="app">
      <header className="hero">
        <div className="hero-content">
          <span className="hero-label">EJERCICIO 4 · REACT + API</span>
          <h1>Conecta</h1>
          <p>
            Un directorio interactivo para consultar usuarios y encontrar
            personas por su nombre.
          </p>

          <div className="hero-caption">
            <span className="caption-dot" />
            Directorio de usuarios
          </div>
        </div>
      </header>

      <main className="main-content">
        <DirectorioUsuarios />
      </main>

      <footer className="footer">
        CONEXION CON API PUBLICA
      </footer>
    </div>
  );
}

export default App;