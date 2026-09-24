import { useEffect, useState } from "react";

function DatosAPI() {

  const [datos, setDatos] = useState([]);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {

    fetch("https://jsonplaceholder.typicode.com/posts?_limit=5")
      .then((respuesta) => respuesta.json())
      .then((informacion) => {
        setDatos(informacion);
        setCargando(false);
      })
      .catch((error) => {
        console.error("Error al obtener los datos:", error);
        setCargando(false);
      });

  }, []);

  if (cargando) {
    return <p>Cargando información...</p>;
  }

  return (
    <section>
      <h2>Información obtenida desde la API</h2>

      {datos.map((dato) => (
        <div key={dato.id}>
          <h3>{dato.title}</h3>
          <p>{dato.body}</p>
        </div>
      ))}
    </section>
  );
}

export default DatosAPI;