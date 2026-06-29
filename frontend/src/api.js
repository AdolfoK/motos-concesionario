import axios from "axios";

// La API se consume de forma relativa: nginx (prod) o el proxy de Vite (dev)
// reenvian /api hacia el backend Django.
const api = axios.create({
  baseURL: "/api",
});

const TOKEN_KEY = "access_token";

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token) {
  if (token) localStorage.setItem(TOKEN_KEY, token);
  else localStorage.removeItem(TOKEN_KEY);
}

export function logout() {
  setToken(null);
}

// Inyecta el token JWT en cada peticion si existe.
api.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
