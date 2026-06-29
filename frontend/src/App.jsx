import { Link, Navigate, Route, Routes, useNavigate } from "react-router-dom";
import { getToken, logout } from "./api.js";
import Catalogo from "./pages/Catalogo.jsx";
import Reserva from "./pages/Reserva.jsx";
import Login from "./pages/Login.jsx";
import AdminPanel from "./pages/AdminPanel.jsx";

function RutaPrivada({ children }) {
  return getToken() ? children : <Navigate to="/login" replace />;
}

export default function App() {
  const navigate = useNavigate();
  const autenticado = Boolean(getToken());

  function cerrarSesion() {
    logout();
    navigate("/login");
  }

  return (
    <div className="app">
      <header className="navbar">
        <Link to="/" className="logo">
          🏍️ MotoStore
        </Link>
        <nav>
          <Link to="/">Catálogo</Link>
          <Link to="/reserva">Reservar hora</Link>
          {autenticado ? (
            <>
              <Link to="/admin">Panel</Link>
              <button className="btn-link" onClick={cerrarSesion}>
                Cerrar sesión
              </button>
            </>
          ) : (
            <Link to="/login">Admin</Link>
          )}
        </nav>
      </header>

      <main className="contenedor">
        <Routes>
          <Route path="/" element={<Catalogo />} />
          <Route path="/reserva" element={<Reserva />} />
          <Route path="/login" element={<Login />} />
          <Route
            path="/admin"
            element={
              <RutaPrivada>
                <AdminPanel />
              </RutaPrivada>
            }
          />
        </Routes>
      </main>

      <footer className="footer">
        Concesionaria de Motos — Arquitectura híbrida Multicloud (demo local)
      </footer>
    </div>
  );
}
