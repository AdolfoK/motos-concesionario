# --- Etapa 1: build con Node (version fijada) ---
FROM node:20-alpine AS build

WORKDIR /app

# Instala dependencias usando el lockfile para builds reproducibles.
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# --- Etapa 2: servir estaticos con nginx (version fijada) ---
FROM nginx:1.25-alpine

# Reemplaza la config por defecto con la nuestra (SPA + proxy a la API).
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
