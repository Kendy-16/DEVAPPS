import { useEffect, useState } from "react";
import TareaLista from "./components/TareaLista";
import FormularioTarea from "./components/FormularioTarea";

function TareasApp() {
  const [tareas, setTareas] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("https://jsonplaceholder.typicode.com/todos?_limit=5")
      .then((respuesta) => {
        if (!respuesta.ok) {
          throw new Error(
            "No se pudieron obtener las tareas"
          );
        }

        return respuesta.json();
      })
      .then((datos) => {

        const transformadas = datos.map((d) => ({
          id: d.id,
          titulo: d.title,
          completada: d.completed,
        }));

        setTareas(transformadas);
      })
      .catch((err) => {
        setError(err.message);
      })
      .finally(() => {
        setCargando(false);
      });
  }, []);

  const alternarTarea = (id) => {
    setTareas(
      tareas.map((t) =>
        t.id === id
          ? {
              ...t,
              completada: !t.completada,
            }
          : t
      )
    );
  };

  const agregarTarea = (titulo) => {

    const nuevaTarea = {
      id: Date.now(),
      titulo,
      completada: false,
    };

    setTareas([...tareas, nuevaTarea]);
  };

  if (cargando) {
    return (
      <p className="mensaje">
        Cargando tareas...
      </p>
    );
  }

  if (error) {
    return (
      <p className="error">
        Ocurrió un error: {error}
      </p>
    );
  }

  return (
    <div>

      <FormularioTarea
        onAgregar={agregarTarea}
      />

      <TareaLista
        tareas={tareas}
        onAlternar={alternarTarea}
      />

    </div>
  );
}

export default TareasApp;