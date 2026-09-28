function TarjetaUsuario({ usuario }) {
  return (
    <article className="user-card">
      <div className="card-heading">
        <div className="avatar" aria-hidden="true">
          {usuario.name.charAt(0)}
        </div>

        <span className="user-number">
          USUARIO #{String(usuario.id).padStart(2, "0")}
        </span>
      </div>

      <h3>{usuario.name}</h3>

      <div className="user-details">
        <div>
          <span className="detail-label">CORREO ELECTRÓNICO</span>
          <a href={`mailto:${usuario.email}`}>{usuario.email}</a>
        </div>

        <div>
          <span className="detail-label">CIUDAD</span>
          <p>{usuario.address.city}</p>
        </div>

        <div>
          <span className="detail-label">EMPRESA</span>
          <p>{usuario.company.name}</p>
        </div>
      </div>
    </article>
  );
}

export default TarjetaUsuario;