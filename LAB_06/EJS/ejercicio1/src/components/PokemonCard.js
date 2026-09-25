function PokemonCard({ pokemon, esFavorito, alCambiarFavorito }) {
  return (
    <article className="pokemon-card">
      <div className="card-top">
        <span className="pokemon-number">
          #{String(pokemon.id).padStart(3, "0")}
        </span>
        <span className="pokemon-category">{pokemon.categoria}</span>
      </div>

      <div className="sprite-area">
        <img
          src={`https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${pokemon.id}.png`}
          alt={`Sprite de ${pokemon.nombre}`}
          className="pokemon-sprite"
        />
      </div>

      <div className="card-content">
        <h2>{pokemon.nombre}</h2>
        <p>{pokemon.descripcion}</p>

        <button
          type="button"
          className={`favorite-button ${esFavorito ? "is-favorite" : ""}`}
          onClick={() => alCambiarFavorito(pokemon.id)}
          aria-pressed={esFavorito}
        >
          {esFavorito ? "★ En favoritos" : "☆ Agregar a favoritos"}
        </button>
      </div>
    </article>
  );
}

export default PokemonCard;