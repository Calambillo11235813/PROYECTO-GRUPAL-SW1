# 🐳 Proyecto SW1 - Docker Setup

Sistema de detección de contenido generado por IA (Texto, Audio, Código) dockerizado.

## 📋 Servicios

- **PostgreSQL 14** - Base de datos (Puerto 5435)
- **Django Backend** - API REST (Puerto 8000)
- **React Frontend** - Interfaz web (Puerto 5173)

## 🚀 Inicio Rápido

### 1. Levantar todos los servicios

```bash
docker-compose up -d
```

### 2. Ver logs

```bash
# Todos los servicios
docker-compose logs -f

# Solo backend
docker-compose logs -f backend

# Solo frontend
docker-compose logs -f frontend
```

### 3. Acceder a las aplicaciones

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **Admin Django:** http://localhost:8000/admin
- **Base de datos:** localhost:5435

## 🛠️ Comandos Útiles

### Detener servicios

```bash
docker-compose down
```

### Reconstruir servicios (después de cambios en Dockerfile)

```bash
docker-compose up -d --build
```

### Reiniciar un servicio específico

```bash
docker-compose restart backend
docker-compose restart frontend
```

### Ejecutar comandos en el backend

```bash
# Crear superusuario
docker-compose exec backend python manage.py createsuperuser

# Aplicar migraciones
docker-compose exec backend python manage.py migrate

# Ejecutar shell de Django
docker-compose exec backend python manage.py shell
```

### Ver estado de servicios

```bash
docker-compose ps
```

### Limpiar todo (contenedores, volúmenes, imágenes)

```bash
docker-compose down -v --rmi all
```

## 🔧 Configuración

### Variables de entorno

Edita el archivo `.env` en la raíz del proyecto:

```env
POSTGRES_DB=proyecto_sw1
POSTGRES_USER=sw1_user
POSTGRES_PASSWORD=sw1_password
SECRET_KEY=tu-secret-key-aqui
```

### Puertos

Si necesitas cambiar los puertos, edita `docker-compose.yml`:

```yaml
ports:
  - "PUERTO_HOST:PUERTO_CONTENEDOR"
```

## 📦 Volúmenes Persistentes

- `postgres_data` - Datos de PostgreSQL
- `backend_media` - Archivos subidos (audio, código, documentos)
- `backend_logs` - Logs de Django

## 🐛 Troubleshooting

### Error: Puerto ya en uso

```bash
# Cambiar puerto en docker-compose.yml o detener el servicio local
# Verificar procesos usando el puerto
netstat -ano | findstr :8000
```

### Backend no se conecta a la base de datos

```bash
# Verificar que la base de datos esté lista
docker-compose logs db

# Reintentar conexión
docker-compose restart backend
```

### Frontend no se conecta al backend

Verifica que `VITE_API_URL` en `docker-compose.yml` apunte a `http://localhost:8000`.

### Reinstalar dependencias

```bash
# Backend
docker-compose exec backend pip install -r requirements.txt

# Frontend
docker-compose exec frontend npm install
```

## 📝 Desarrollo

### Modo desarrollo con hot-reload

Los volúmenes están configurados para sincronizar cambios automáticamente:

- **Backend:** Django runserver detecta cambios en Python
- **Frontend:** Vite detecta cambios en React

### Agregar nuevas dependencias

**Backend:**

1. Agrega el paquete a `Backend/requirements.txt`
2. Reconstruye: `docker-compose up -d --build backend`

**Frontend:**

1. Agrega el paquete: `docker-compose exec frontend npm install nombre-paquete`
2. Actualiza `package.json` si es necesario

## 🚀 Producción

Para producción, modifica:

1. **Backend Dockerfile:** Usar gunicorn/uvicorn
2. **Frontend Dockerfile:** Build estático + nginx
3. **docker-compose.yml:** Agregar nginx reverse proxy
4. **Variables de entorno:** `DEBUG=False`, SECRET_KEY segura

## 📚 Estructura

```
.
├── Backend/
│   ├── Dockerfile
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   └── src/
├── docker-compose.yml
├── .env
└── README_DOCKER.md
```

## ✅ Checklist de Inicio

- [ ] Instalar Docker Desktop
- [ ] Clonar repositorio
- [ ] Crear archivo `.env`
- [ ] Ejecutar `docker-compose up -d`
- [ ] Esperar a que todos los servicios estén healthy
- [ ] Acceder a http://localhost:5173
- [ ] Crear superusuario si es necesario

## 🎯 Próximos Pasos

1. Crear superusuario: `docker-compose exec backend python manage.py createsuperuser`
2. Acceder al admin: http://localhost:8000/admin
3. Comenzar a usar la aplicación en http://localhost:5173
