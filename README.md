# SIRA – Sistema de Recomendaciones Académicas

## Estructura del proyecto

```
sira/
├── backend/
│   ├── main.py              ← Entrada de la API
│   ├── database.py          ← Conexión a MySQL
│   ├── requirements.txt     ← Dependencias Python
│   ├── Procfile             ← Para despliegue en Render
│   ├── .env.example         ← Variables de entorno (copia como .env)
│   └── routers/
│       ├── estudiantes.py   ← CRUD + Login
│       ├── materias.py      ← CRUD materias
│       ├── calificaciones.py← CRUD calificaciones
│       └── carreras.py      ← CRUD carreras
└── frontend/
    └── index.html           ← App web completa (abre en el navegador)
```

---

## 1. Configurar el Backend (FastAPI)

### Requisitos
- Python 3.10+
- MySQL corriendo con la BD `sira`

### Pasos

```bash
cd backend

# Crea el entorno virtual
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# Instala dependencias
pip install -r requirements.txt

# Copia el .env
cp .env.example .env
# Edita .env con tus datos de MySQL

# Inicia el servidor
uvicorn main:app --reload
```

La API queda en: http://localhost:8000  
Documentación automática: http://localhost:8000/docs

---

## 2. Configurar la Base de Datos MySQL

Crea los schemas y tablas según el diagrama S.I.R.A.pdf.
Asegúrate de que los schemas existan:
- `academico` (tablas: carrera, materia, plan_estudios_carrera)
- `estudiantes` (tablas: estudiante, inscripcion_materia)
- `evaluacion` (tablas: calificacion_materia, nivel_rendimiento)
- `recomendaciones` (las demás tablas)

---

## 3. Usar el Frontend

### En local
Abre `frontend/index.html` directamente en el navegador.

### Cambiar la URL de la API
En `frontend/index.html`, línea donde dice:
```js
const API = "http://localhost:8000/api";
```
Cámbiala a tu URL de Render:
```js
const API = "https://tu-app.onrender.com/api";
```

### En Android
1. Despliega `frontend/index.html` en cualquier hosting estático:
   - GitHub Pages (gratis)
   - Netlify (gratis, arrastra la carpeta)
   - Render Static Site
2. Abre la URL en el navegador de Android → funciona como app web.

---

## 4. Desplegar en Render

### Backend (Web Service)
1. Sube el proyecto a GitHub
2. Crea nuevo **Web Service** en render.com
3. Conecta tu repositorio
4. Configuración:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Agrega las variables de entorno (DB_HOST, DB_USER, etc.)

### Frontend
1. Crea un **Static Site** en Render
2. **Root Directory**: `frontend`
3. No necesita build command

---

## 5. Endpoints disponibles

| Método | Endpoint                          | Descripción              |
|--------|-----------------------------------|--------------------------|
| POST   | /api/estudiantes/login            | Login estudiante         |
| GET    | /api/estudiantes/                 | Listar estudiantes       |
| POST   | /api/estudiantes/                 | Crear estudiante         |
| PUT    | /api/estudiantes/{id}             | Actualizar estudiante    |
| DELETE | /api/estudiantes/{id}             | Eliminar estudiante      |
| GET    | /api/materias/                    | Listar materias          |
| POST   | /api/materias/                    | Crear materia            |
| PUT    | /api/materias/{id}                | Actualizar materia       |
| DELETE | /api/materias/{id}                | Eliminar materia         |
| GET    | /api/calificaciones/              | Listar calificaciones    |
| GET    | /api/calificaciones/estudiante/{id}| Calificaciones por alumno|
| POST   | /api/calificaciones/              | Crear calificación       |
| PUT    | /api/calificaciones/{id}          | Actualizar calificación  |
| DELETE | /api/calificaciones/{id}          | Eliminar calificación    |
| GET    | /api/carreras/                    | Listar carreras          |
| POST   | /api/carreras/                    | Crear carrera            |
| PUT    | /api/carreras/{id}                | Actualizar carrera       |
| DELETE | /api/carreras/{id}                | Eliminar carrera         |

---

## Contexto para GitHub Copilot

Este proyecto es una API REST en **FastAPI + MySQL** para el Sistema de Recomendaciones Académicas (SIRA).
- Usa `mysql-connector-python` con connection pooling
- Los schemas de MySQL son: `academico`, `estudiantes`, `evaluacion`, `recomendaciones`
- Todos los endpoints siguen el patrón CRUD estándar
- El frontend es un HTML/CSS/JS vanilla sin frameworks
- Para agregar un nuevo módulo: crea `routers/nuevo.py` e inclúyelo en `main.py`
