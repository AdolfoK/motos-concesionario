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

  if (cargando) return <p>Cargando catálogo...</p>;
  if (error) return <p className="error">{error}</p>;

  return (
    <section>
      <h1>Catálogo de motos</h1>
      {motos.length === 0 && <p>No hay motos disponibles por el momento.</p>}
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
