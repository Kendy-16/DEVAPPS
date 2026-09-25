import { useEffect, useState } from "react";

function ListaUsuarios() {
  const [usuarios, setUsuarios] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const controlador = new AbortController();

    async function consultarUsuarios() {
      try {
        const respuesta = await fetch(
          "https://jsonplaceholder.typicode.com/users",
          { signal: controlador.signal }
        );

        if (!respuesta.ok) {
          throw new Error("No se pudo consultar la API.");
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

    consultarUsuarios();

    return () => controlador.abort();
  }, []);

  return (
    <section className="panel api-panel">
      <div className="panel-heading">
        <span className="panel-icon">⌁</span>
        <div>
          <span className="section-label">CONSULTA EXTERNA</span>
          <h2>Usuarios de la API</h2>
        </div>
      </div>

      {cargando && (
        <p className="status-message" role="status">
          Consultando usuarios...
        </p>
      )}

      {error && <p className="status-message error-message">{error}</p>}

      {!cargando && !error && (
        <div className="usuarios-lista">
          {usuarios.map((usuario) => (
            <article className="usuario-item" key={usuario.id}>
              <div className="avatar" aria-hidden="true">
                {usuario.name.charAt(0)}
              </div>

              <div className="usuario-info">
                <h3>{usuario.name}</h3>
                <p>{usuario.email}</p>
                <span>⌖ {usuario.address.city}</span>
              </div>

              <span className="api-badge">API</span>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}

export default ListaUsuarios;