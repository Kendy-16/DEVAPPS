import { useState } from "react";
import ProyectoCard from "./components/ProyectoCard";
import "./App.css";

const proyectosIniciales = [
  {
    id: 1,
    nombre: "Portal académico",
    descripcion: "Diseñar una plataforma para consultar cursos, horarios y calificaciones.",
    estado: "Pendiente",
  },
  {
    id: 2,
    nombre: "Sistema de inventario",
    descripcion: "Registrar productos y controlar las entradas y salidas del almacén.",
    estado: "En curso",
  },
  {
    id: 3,
    nombre: "Aplicación de reservas",
    descripcion: "Permitir que los clientes consulten disponibilidad y registren reservas.",
    estado: "Finalizado",
  },
  {
    id: 4,
    nombre: "Panel de ventas",
    descripcion: "Mostrar indicadores y reportes de ventas para la empresa.",
    estado: "Pendiente",
  },
  {
    id: 5,
    nombre: "Gestor de incidencias",
    descripcion: "Organizar y dar seguimiento a solicitudes de soporte técnico.",
    estado: "En curso",
  },
  {
    id: 6,
    nombre: "Biblioteca digital",
    descripcion: "Facilitar la búsqueda y consulta de libros del catálogo.",
    estado: "Pendiente",
  },
];

const siguientesEstados = {
  Pendiente: "En curso",
  "En curso": "Finalizado",
  Finalizado: "Pendiente",
};

function App() {
  const [proyectos, setProyectos] = useState(proyectosIniciales);

  function cambiarEstado(id) {
    setProyectos((anteriores) =>
      anteriores.map((proyecto) =>
        proyecto.id === id
          ? {
              ...proyecto,
              estado: siguientesEstados[proyecto.estado],
            }
          : proyecto
      )
    );
  }

  function eliminarProyecto(id) {
    setProyectos((anteriores) =>
      anteriores.filter((proyecto) => proyecto.id !== id)
    );
  }

  const pendientes = proyectos.filter(
    (proyecto) => proyecto.estado === "Pendiente"
  ).length;

  const enCurso = proyectos.filter(
    (proyecto) => proyecto.estado === "En curso"
  ).length;

  const finalizados = proyectos.filter(
    (proyecto) => proyecto.estado === "Finalizado"
  ).length;

  return (
    <div className="app">
      <header className="hero">
        <div className="hero-content">
          <span className="hero-label">PANEL INTERACTIVO · REACT</span>
          <h1>ProjectFlow</h1>
          <p>
            Consulta tus proyectos, actualiza su progreso y mantén organizada
            tu colección.
          </p>
        </div>
      </header>

      <main className="main-content">
        <section className="overview" aria-label="Resumen de proyectos">
          <div className="overview-heading">
            <span className="section-label">VISTA GENERAL</span>
            <h2>Estado de los proyectos</h2>
            <p>Los indicadores cambian cuando actualizas o eliminas un proyecto.</p>
          </div>

          <div className="stats-grid">
            <div className="stat-card">
              <span>Total</span>
              <strong>{proyectos.length}</strong>
            </div>
            <div className="stat-card pendiente">
              <span>Pendientes</span>
              <strong>{pendientes}</strong>
            </div>
            <div className="stat-card en-curso">
              <span>En curso</span>
              <strong>{enCurso}</strong>
            </div>
            <div className="stat-card finalizado">
              <span>Finalizados</span>
              <strong>{finalizados}</strong>
            </div>
          </div>
        </section>

        <section className="collection">
          <div className="collection-heading">
            <div>
              <span className="section-label">COLECCIÓN</span>
              <h2>Todos los proyectos</h2>
            </div>
            <span className="collection-count">{proyectos.length} proyectos</span>
          </div>

          {proyectos.length > 0 ? (
            <div className="projects-grid">
              {proyectos.map((proyecto) => (
                <ProyectoCard
                  key={proyecto.id}
                  proyecto={proyecto}
                  onCambiarEstado={cambiarEstado}
                  onEliminar={eliminarProyecto}
                />
              ))}
            </div>
          ) : (
            <div className="empty-state">
              <span aria-hidden="true">◇</span>
              <h3>No quedan proyectos</h3>
              <p>Has eliminado todos los elementos de la colección.</p>
            </div>
          )}
        </section>
      </main>

      <footer className="footer">ProjectFlow · Ejercicio 3 de React</footer>
    </div>
  );
}

export default App;