import { useEffect, useState } from "react";
import api from "../api.js";

const FORM_VACIO = {
  marca: "",
  modelo: "",
  cilindrada: "",
  precio: "",
  stock: "",
  descripcion: "",
};

export default function AdminPanel() {
  const [motos, setMotos] = useState([]);
  const [form, setForm] = useState(FORM_VACIO);
  const [imagen, setImagen] = useState(null);
  const [editandoId, setEditandoId] = useState(null);
  const [error, setError] = useState("");
  const [cargando, setCargando] = useState(true);

  function cargar() {
    setCargando(true);
    api
      .get("/motos/")
      .then((res) => setMotos(res.data.results ?? res.data))
      .catch(() => setError("No se pudo cargar el catálogo."))
      .finally(() => setCargando(false));
  }

  useEffect(cargar, []);

  function actualizar(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  function resetear() {
    setForm(FORM_VACIO);
    setImagen(null);
    setEditandoId(null);
    setError("");
  }

  function editar(moto) {
    setEditandoId(moto.id);
    setForm({
      marca: moto.marca,
      modelo: moto.modelo,
      cilindrada: moto.cilindrada,
      precio: moto.precio,
      stock: moto.stock,
      descripcion: moto.descripcion ?? "",
    });
    setImagen(null);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  async function guardar(e) {
    e.preventDefault();
    setError("");
    // Si hay imagen se envia como multipart; si no, JSON simple.
    let payload = form;
    let config = {};
    if (imagen) {
      const fd = new FormData();
      Object.entries(form).forEach(([k, v]) => fd.append(k, v));
      fd.append("imagen", imagen);
      payload = fd;
      config = { headers: { "Content-Type": "multipart/form-data" } };
    }
    try {
      if (editandoId) {
        await api.patch(`/motos/${editandoId}/`, payload, config);
      } else {
        await api.post("/motos/", payload, config);
      }
      resetear();
      cargar();
    } catch (err) {
      setError("No se pudo guardar. Revisa los campos.");
    }
  }

  async function eliminar(id) {
    if (!window.confirm("¿Eliminar esta moto del catálogo?")) return;
    try {
      await api.delete(`/motos/${id}/`);
      cargar();
    } catch (err) {
      setError("No se pudo eliminar.");
    }
  }

  return (
    <section>
      <h1>Panel de administración — Catálogo</h1>
      {error && <p className="error">{error}</p>}

      <form className="formulario" onSubmit={guardar}>
        <h2>{editandoId ? "Editar moto" : "Nueva moto"}</h2>
        <div className="fila">
          <label>
            Marca
            <input name="marca" value={form.marca} onChange={actualizar} required />
          </label>
          <label>
            Modelo
            <input name="modelo" value={form.modelo} onChange={actualizar} required />
          </label>
        </div>
        <div className="fila">
          <label>
            Cilindrada (cc)
            <input
              type="number"
              name="cilindrada"
              value={form.cilindrada}
              onChange={actualizar}
              required
            />
          </label>
          <label>
            Precio (CLP)
            <input
              type="number"
              name="precio"
              value={form.precio}
              onChange={actualizar}
              required
            />
          </label>
          <label>
            Stock
            <input
              type="number"
              name="stock"
              value={form.stock}
              onChange={actualizar}
              required
            />
          </label>
        </div>
        <label>
          Descripción
          <textarea
            name="descripcion"
            value={form.descripcion}
            onChange={actualizar}
            rows={2}
          />
        </label>
        <label>
          Imagen
          <input
            type="file"
            accept="image/*"
            onChange={(e) => setImagen(e.target.files[0] ?? null)}
          />
        </label>
        <div className="acciones">
          <button className="btn" type="submit">
            {editandoId ? "Guardar cambios" : "Crear moto"}
          </button>
          {editandoId && (
            <button type="button" className="btn-secundario" onClick={resetear}>
              Cancelar
            </button>
          )}
        </div>
      </form>

      <h2>Motos en catálogo</h2>
      {cargando ? (
        <p>Cargando...</p>
      ) : (
        <table className="tabla">
          <thead>
            <tr>
              <th>Marca</th>
              <th>Modelo</th>
              <th>cc</th>
              <th>Precio</th>
              <th>Stock</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {motos.map((m) => (
              <tr key={m.id}>
                <td>{m.marca}</td>
                <td>{m.modelo}</td>
                <td>{m.cilindrada}</td>
                <td>{Number(m.precio).toLocaleString("es-CL")}</td>
                <td>{m.stock}</td>
                <td className="acciones">
                  <button className="btn-secundario" onClick={() => editar(m)}>
                    Editar
                  </button>
                  <button className="btn-peligro" onClick={() => eliminar(m.id)}>
                    Eliminar
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
}
