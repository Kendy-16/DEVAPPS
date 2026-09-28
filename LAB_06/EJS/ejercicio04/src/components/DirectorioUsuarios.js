import { useEffect, useState } from "react";
import TarjetaUsuario from "./TarjetaUsuario";

function DirectorioUsuarios() {
  const [usuarios, setUsuarios] = useState([]);
  const [busqueda, setBusqueda] = useState("");
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const controlador = new AbortController();

    async function obtenerUsuarios() {
      try {
        const respuesta = await fetch(
          "https://jsonplaceholder.typicode.com/users",
          { signal: controlador.signal }
        );

        if (!respuesta.ok) {
          throw new Error("La solicitud no se pudo completar.");
        }

        const datos = await respuesta.json();
        setUsuarios(datos);
      } catch (problema) {
        if (problema.name !== "AbortError") {
          setError("No se pudieron cargar los usuarios. Revisa tu conexión.");
        }
      } finally {
        if (!controlador.signal.aborted) {
          setCargando(false);
        }
      }
    }

    obtenerUsuarios();

    return () => controlador.abort();
  }, []);

  const usuariosFiltrados = usuarios.filter((usuario) =>
    usuario.name.toLowerCase().includes(busqueda.trim().toLowerCase())
  );

  return (
    <section className="directory">
      <div className="directory-heading">
        <div>
          <span className="section-label">EXPLORA EL DIRECTORIO</span>
          <h2>Personas y conexiones</h2>
          <p>Busca por nombre para encontrar rápidamente a un usuario.</p>
        </div>

        {!cargando && !error && (
          <span className="results-count">
            {usuariosFiltrados.length} de {usuarios.length} usuarios
          </span>
        )}
      </div>

      <div className="search-panel">
        <label htmlFor="buscar-usuario">Buscar usuario por nombre</label>

        <div className="search-field">
          <span aria-hidden="true">⌕</span>
          <input
            id="buscar-usuario"
            type="search"
            placeholder="Escribe un nombre..."
            value={busqueda}
            onChange={(event) => setBusqueda(event.target.value)}
          />
        </div>
      </div>

      {cargando && (
        <div className="message-card" role="status">
          <span className="message-icon" aria-hidden="true">◌</span>
          <h3>Cargando información...</h3>
          <p>Estamos consultando los usuarios de la API.</p>
        </div>
      )}

      {error && (
        <div className="message-card error-card" role="alert">
          <span className="message-icon" aria-hidden="true">!</span>
          <h3>No fue posible cargar el directorio</h3>
          <p>{error}</p>
        </div>
      )}

      {!cargando && !error && usuariosFiltrados.length === 0 && (
        <div className="message-card">
          <span className="message-icon" aria-hidden="true">⌕</span>
          <h3>Sin coincidencias</h3>
          <p>
            {busqueda.trim()
              ? `No encontramos usuarios con el nombre «${busqueda.trim()}».`
              : "La API no devolvió usuarios para mostrar."}
          </p>
        </div>
      )}

      {!cargando && !error && usuariosFiltrados.length > 0 && (
        <div className="users-grid">
          {usuariosFiltrados.map((usuario) => (
            <TarjetaUsuario key={usuario.id} usuario={usuario} />
          ))}
        </div>
      )}
    </section>
  );
}

export default DirectorioUsuarios;