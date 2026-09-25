import { useState } from "react";
import FormularioRegistro from "./components/FormularioRegistro";
import ListaUsuarios from "./components/ListaUsuarios";
import "./App.css";

function App() {
  const [registros, setRegistros] = useState([]);

  function agregarRegistro(datos) {
    const nuevoRegistro = {
      id: crypto.randomUUID(),
      ...datos,
    };

    setRegistros((anteriores) => [nuevoRegistro, ...anteriores]);
  }

  return (
    <div className="app">
      <header className="hero">
        <div className="hero-content">
          <span className="hero-tag">SISTEMA DE REGISTRO · REACT</span>
          <h1>BlueData</h1>
          <p>
            Registrar información y consultas desde una API
          </p>

          <div className="hero-line">
            <span>FORMULARIO</span>
            <span>+</span>
            <span>CONSULTAS EN API</span>
          </div>
        </div>
      </header>

      <main className="main-content">
        <div className="intro">
          <span className="section-label">PANEL PRINCIPAL</span>
          <h2>Registro y consulta de información</h2>
        </div>

        <div className="dashboard-grid">
          <div>
            <FormularioRegistro onRegistrar={agregarRegistro} />

            <section className="panel registrados-panel">
              <div className="panel-heading">
                <span className="panel-icon">▤</span>
                <div>
                  <span className="section-label">DATOS INGRESADOS</span>
                  <h2>Registros recientes</h2>
                </div>
                <span className="count-badge">{registros.length}</span>
              </div>

              {registros.length === 0 ? (
                <p className="empty-message">
                  Todavía no hay registros. Completa el formulario para
                  agregar el primero.
                </p>
              ) : (
                <div className="registros-lista">
                  {registros.map((registro) => (
                    <article className="registro-item" key={registro.id}>
                      <h3>{registro.nombre}</h3>
                      <p>{registro.correo}</p>
                      <span>⌖ {registro.ciudad}</span>
                    </article>
                  ))}
                </div>
              )}
            </section>
          </div>

          <ListaUsuarios />
        </div>
      </main>

      <footer className="footer">
        FORMULARIO
      </footer>
    </div>
  );
}

export default App;