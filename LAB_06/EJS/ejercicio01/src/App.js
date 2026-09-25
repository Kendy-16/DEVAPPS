import { useState } from "react";
import PokemonCard from "./components/PokemonCard";
import "./App.css";

let pokemonsIniciales = [
  {
    id: 701,
    nombre: "Hawlucha",
    descripcion: "Un luchador ágil que combina movimientos aéreos con técnicas de combate.",
    categoria: "Lucha · Volador",
  },
  {
    id: 483,
    nombre: "Dialga",
    descripcion: "Pokémon legendario asociado con el control del tiempo.",
    categoria: "Acero · Dragón",
  },
  {
    id: 484,
    nombre: "Palkia",
    descripcion: "Pokémon legendario capaz de alterar el espacio.",
    categoria: "Agua · Dragón",
  },
  {
    id: 260,
    nombre: "Swampert",
    descripcion: "Un poderoso Pokémon que se desplaza con facilidad por tierra y agua.",
    categoria: "Agua · Tierra",
  },
  {
    id: 279,
    nombre: "Pelipper",
    descripcion: "Sobrevuela las costas y transporta objetos en su gran pico.",
    categoria: "Agua · Volador",
  },
  {
    id: 254,
    nombre: "Sceptile",
    descripcion: "Se mueve velozmente entre los árboles y protege su territorio.",
    categoria: "Planta",
  },
  {
    id: 384,
    nombre: "Rayquaza",
    descripcion: "Un Pokémon legendario que habita en las alturas del cielo.",
    categoria: "Dragón · Volador",
  },
];

function App() {
  const [favoritos, setFavoritos] = useState([]);
  const [mostrarSoloFavoritos, setMostrarSoloFavoritos] = useState(false);

  function cambiarFavorito(id) {
    setFavoritos((anteriores) =>
      anteriores.includes(id)
        ? anteriores.filter((favoritoId) => favoritoId !== id)
        : [...anteriores, id]
    );
  }

  const pokemonsVisibles = mostrarSoloFavoritos
    ? pokemonsIniciales.filter((pokemon) => favoritos.includes(pokemon.id))
    : pokemonsIniciales;

  return (
    <div className="app">
      <header className="hero">
        <div className="hero-content">
          <span className="eyebrow">EXPEDICIÓN POKÉMON</span>
          <h1>Safari Pokédex</h1>
          <p>
            Explora la colección y guarda a tus Pokémon favoritos para
            encontrarlos rápidamente.
          </p>

          <div className="hero-stats">
            <span>◈ {pokemonsIniciales.length} Pokémon</span>
            <span>★ {favoritos.length} favoritos</span>
          </div>
        </div>
      </header>

      <main className="main-content">
        <div className="section-heading">
          <div>
            <span className="section-label">CUADERNO DE CAMPO</span>
            <h2>Explora la colección</h2>
          </div>

          <button
            type="button"
            className="filter-button"
            onClick={() => setMostrarSoloFavoritos((valor) => !valor)}
            aria-pressed={mostrarSoloFavoritos}
          >
            {mostrarSoloFavoritos ? "Ver todos" : "★ Ver favoritos"}
          </button>
        </div>

        {pokemonsVisibles.length > 0 ? (
          <div className="pokemon-grid">
            {pokemonsVisibles.map((pokemon) => (
              <PokemonCard
                key={pokemon.id}
                pokemon={pokemon}
                esFavorito={favoritos.includes(pokemon.id)}
                alCambiarFavorito={cambiarFavorito}
              />
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <span>🌿</span>
            <h3>Aún no tienes favoritos</h3>
            <p>Vuelve a la colección y marca los Pokémon que más te gusten.</p>
          </div>
        )}
      </main>

      <footer className="footer">
        Safari Pokédex
      </footer>
    </div>
  );
}

export default App;