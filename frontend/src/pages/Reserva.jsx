import { useState } from "react";
import api from "../api.js";

const TIPOS_SERVICIO = [
  { value: "mantencion", label: "Mantención" },
  { value: "revision_tecnica", label: "Revisión técnica" },
  { value: "reparacion", label: "Reparación" },
];

const BLOQUES = [
  "09:00-10:00",
  "10:00-11:00",
  "11:00-12:00",
  "12:00-13:00",
  "15:00-16:00",
  "16:00-17:00",
  "17:00-18:00",
];

const ESTADO_INICIAL = {
  nombre_cliente: "",
  telefono: "",
  tipo_servicio: "mantencion",
  fecha: "",
  bloque_horario: BLOQUES[0],
  moto_marca: "",
  moto_modelo: "",
  patente: "",
  comentario: "",
};

export default function Reserva() {
  const [form, setForm] = useState(ESTADO_INICIAL);
  const [enviando, setEnviando] = useState(false);
  const [error, setError] = useState("");
  const [resultado, setResultado] = useState(null);

  function actualizar(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function enviar(e) {
    e.preventDefault();
    setError("");
    setEnviando(true);
    try {
      const { data } = await api.post("/reservas/", form);
      setResultado(data);
      // Abre WhatsApp con el mensaje pre-llenado en una pestaña nueva.
      if (data.whatsapp_url) {
        window.open(data.whatsapp_url, "_blank", "noopener");
      }
    } catch (err) {
      setError(
        "No se pudo registrar la reserva. Revisa los datos e inténtalo nuevamente."
      );
    } finally {
      setEnviando(false);
    }
  }

  if (resultado) {
    return (
      <section className="reserva-ok">
        <h1>¡Solicitud registrada! ✅</h1>
        <p>
          Tu solicitud de hora (#{resultado.id}) quedó guardada. Te abrimos
          WhatsApp para que confirmes con la concesionaria.
        </p>
        <p>Si no se abrió automáticamente, usa este botón:</p>
        <a
          className="btn btn-whatsapp"
          href={resultado.whatsapp_url}
          target="_blank"
          rel="noopener noreferrer"
        >
          Continuar en WhatsApp
        </a>
        <p>
          <button
            className="btn-link"
            onClick={() => {
              setResultado(null);
              setForm(ESTADO_INICIAL);
            }}
          >
            Hacer otra reserva
          </button>
        </p>
      </section>
    );
  }

  return (
    <section>
      <h1>Reservar hora de servicio técnico</h1>
      <p className="subtitulo">
        Completa el formulario y confirma tu hora por WhatsApp.
      </p>
      {error && <p className="error">{error}</p>}
      <form className="formulario" onSubmit={enviar}>
        <label>
          Nombre completo
          <input
            name="nombre_cliente"
            value={form.nombre_cliente}
            onChange={actualizar}
            required
          />
        </label>

        <label>
          Teléfono de contacto
          <input
            name="telefono"
            value={form.telefono}
            onChange={actualizar}
            placeholder="+56 9 1234 5678"
            required
          />
        </label>

        <label>
          Tipo de servicio
          <select
            name="tipo_servicio"
            value={form.tipo_servicio}
            onChange={actualizar}
          >
            {TIPOS_SERVICIO.map((t) => (
              <option key={t.value} value={t.value}>
                {t.label}
              </option>
            ))}
          </select>
        </label>

        <div className="fila">
          <label>
            Fecha
            <input
              type="date"
              name="fecha"
              value={form.fecha}
              onChange={actualizar}
              required
            />
          </label>
          <label>
            Bloque horario
            <select
              name="bloque_horario"
              value={form.bloque_horario}
              onChange={actualizar}
            >
              {BLOQUES.map((b) => (
                <option key={b} value={b}>
                  {b}
                </option>
              ))}
            </select>
          </label>
        </div>

        <div className="fila">
          <label>
            Marca de la moto
            <input
              name="moto_marca"
              value={form.moto_marca}
              onChange={actualizar}
              required
            />
          </label>
          <label>
            Modelo
            <input
              name="moto_modelo"
              value={form.moto_modelo}
              onChange={actualizar}
              required
            />
          </label>
        </div>

        <label>
          Patente (opcional)
          <input name="patente" value={form.patente} onChange={actualizar} />
        </label>

        <label>
          Comentario (opcional)
          <textarea
            name="comentario"
            value={form.comentario}
            onChange={actualizar}
            rows={3}
          />
        </label>

        <button className="btn btn-whatsapp" type="submit" disabled={enviando}>
          {enviando ? "Enviando..." : "Reservar por WhatsApp"}
        </button>
      </form>
    </section>
  );
}
