import { useState } from "react";

import Header from "./components/Header";
import Card from "./components/Card";
import Footer from "./components/Footer";
import Formulario from "./components/Formulario";
import DatosAPI from "./components/DatosAPI";

const tarjetasIniciales = [
  {
    id: 1,
    nombre: "React",
    descripcion: "Biblioteca de JavaScript utilizada para crear interfaces de usuario.",
    categoria: "Frontend"
  },
  {
    id: 2,
    nombre: "Vite",
    descripcion: "Herramienta utilizada para crear y ejecutar proyectos modernos de desarrollo web.",
    categoria: "Herramienta de desarrollo"
  },
  {
    id: 3,
    nombre: "JSX",
    descripcion: "Sintaxis que permite escribir estructuras similares a HTML dentro de JavaScript.",
    categoria: "Tecnología"
  },
  {
    id: 4,
    nombre: "JavaScript",
    descripcion: "Lenguaje de programación utilizado para agregar lógica e interactividad a las aplicaciones web.",
    categoria: "Lenguaje"
  }
];

function App() {

  const [tarjetaSeleccionada, setTarjetaSeleccionada] = useState(null);

  const [tarjetas, setTarjetas] = useState(tarjetasIniciales);

  function agregarTarjeta(nuevaTarjeta) {

    const nuevaTarjetaCompleta = {
      id: Date.now(),
      nombre: nuevaTarjeta.nombre,
      descripcion: nuevaTarjeta.descripcion,
      categoria: "Agregado por usuario"
    };

    setTarjetas([...tarjetas, nuevaTarjetaCompleta]);
  }

  return (
    <div className="contenedor">

      <Header />

      <Formulario onAgregar={agregarTarjeta} />

      <main>

        {tarjetas.map((tarjeta) => (
          <Card
            key={tarjeta.id}
            nombre={tarjeta.nombre}
            descripcion={tarjeta.descripcion}
            categoria={tarjeta.categoria}
            seleccionada={tarjetaSeleccionada === tarjeta.id}
            onSeleccionar={() => setTarjetaSeleccionada(tarjeta.id)}
          />
        ))}

      </main>

      <DatosAPI />

      <Footer />

    </div>
  );
}

export default App;