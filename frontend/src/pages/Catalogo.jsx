import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api.js";

function formatoPrecio(valor) {
  return new Intl.NumberFormat("es-CL", {
    style: "currency",
    currency: "CLP",
    maximumFractionDigits: 0,
  }).format(valor);
}

export default function Catalogo() {
  const [motos, setMotos] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .get("/motos/")
      .then((res) => setMotos(res.data.results ?? res.data))
      .catch(() => setError("No se pudo cargar el catálogo."))
      .finally(() => setCargando(false));
  }, []);

  return (
    <section>
      <div className="hero">
        <div className="hero-content">
          <p className="hero-kicker">MotoStore</p>
          <h1 className="hero-title">
            Excelencia sobre <span className="acento">dos ruedas</span>
          </h1>
          <p className="hero-sub">
            Descubre nuestra selección premium de motocicletas y agenda tu hora
            de servicio técnico en minutos, directo por WhatsApp.
          </p>
          <a className="btn" href="#catalogo">
            Ver catálogo
          </a>
        </div>
      </div>

      <h2 id="catalogo" className="seccion-titulo">
        Catálogo
      </h2>
      <hr className="seccion-linea" />

      {cargando && <p className="cargando">Cargando catálogo...</p>}
      {error && <p className="error">{error}</p>}
      {!cargando && !error && motos.length === 0 && (
        <p className="cargando">No hay motos disponibles por el momento.</p>
      )}

      <div className="grid">
        {motos.map((moto) => (
          <article key={moto.id} className="card">
            <div className="card-img">
              {moto.imagen_url ? (
                <img src={moto.imagen_url} alt={`${moto.marca} ${moto.modelo}`} />
              ) : (
                <div className="placeholder">🏍️</div>
              )}
            </div>
            <div className="card-body">
              <h3>
                {moto.marca} {moto.modelo}
              </h3>
              <p className="cc">{moto.cilindrada} cc</p>
              {moto.descripcion && <p className="desc">{moto.descripcion}</p>}
              <p className="precio">{formatoPrecio(moto.precio)}</p>
              <p className={moto.stock > 0 ? "stock" : "stock agotado"}>
                {moto.stock > 0 ? `Stock: ${moto.stock}` : "Sin stock"}
              </p>
              <Link className="btn" to="/reserva">
                Reservar servicio
              </Link>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
