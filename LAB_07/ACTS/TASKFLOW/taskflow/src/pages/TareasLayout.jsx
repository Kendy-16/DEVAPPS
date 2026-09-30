import { Outlet } from "react-router-dom";

function TareasLayout() {
  return (
    <section className="tareas-contenedor">

      <Outlet />

    </section>
  );
}

export default TareasLayout;