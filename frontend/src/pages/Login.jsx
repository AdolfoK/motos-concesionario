import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api, { setToken } from "../api.js";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [enviando, setEnviando] = useState(false);
  const navigate = useNavigate();

  async function enviar(e) {
    e.preventDefault();
    setError("");
    setEnviando(true);
    try {
      const { data } = await api.post("/auth/login/", { username, password });
      setToken(data.access);
      navigate("/admin");
    } catch (err) {
      setError("Credenciales inválidas.");
    } finally {
      setEnviando(false);
    }
  }

  return (
    <section className="login">
      <h1>Acceso administrador</h1>
      {error && <p className="error">{error}</p>}
      <form className="formulario" onSubmit={enviar}>
        <label>
          Usuario
          <input
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </label>
        <label>
          Contraseña
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </label>
        <button className="btn" type="submit" disabled={enviando}>
          {enviando ? "Ingresando..." : "Ingresar"}
        </button>
      </form>
      <p className="hint">Demo local: admin / admin123</p>
    </section>
  );
}
