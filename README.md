# Chambeapp

Aplicación web de gestión de proyectos y tareas con tableros estilo Kanban.

---

## Tecnologías utilizadas

### Frontend

| Tecnología      | Versión   | Uso                                    |
| --------------- | --------- | -------------------------------------- |
| React           | `^19.2.8` | Construcción de la interfaz de usuario |
| Vite            | `^8.3.0`  | Servidor de desarrollo y empaquetado   |
| TypeScript      | `~6.0.2`  | Tipado estático de la aplicación       |
| React Router    | `^7.18.4` | Enrutado del lado del cliente          |
| Tailwind CSS    | `^4.3.3`  | Estilos y diseño responsivo            |
| shadcn/ui       | `^4.21.0` | Componentes de interfaz reutilizables  |
| React Hook Form | `^7.88.0` | Gestión de formularios                 |
| Axios           | `^1.20.0` | Cliente HTTP hacia la API              |
| Lucide React    | `^1.47.0` | Iconografía                            |
| pnpm            | —         | Gestor de paquetes                     |

### Backend

| Tecnología | Versión             | Uso                                        |
| ---------- | ------------------- | ------------------------------------------ |
| Python     | `3.12` (contenedor) | Lenguaje del servicio                      |
| FastAPI    | `0.110.0`           | Framework de la API REST                   |
| Uvicorn    | `0.29.0`            | Servidor ASGI                              |
| SQLAlchemy | `2.0.28`            | ORM y acceso a datos                       |
| Pydantic   | —                   | Validación de datos y esquemas             |
| PyJWT      | `2.14.0`            | Generación y validación de tokens          |
| Passlib    | `1.7.4`             | Hash de contraseñas                        |
| debugpy    | `1.8.1`             | Depuración remota en el contenedor         |
| Mailtrap   | —                   | Envío de correos en entornos de desarrollo |

### Base de datos

| Tecnología | Versión     | Uso                                                   |
| ---------- | ----------- | ----------------------------------------------------- |
| PostgreSQL | `16-alpine` | Persistencia de usuarios, tableros, columnas y tareas |
| psycopg    | `3.1.18`    | Driver de conexión                                    |

### Infraestructura

| Tecnología     | Uso                                           |
| -------------- | --------------------------------------------- |
| Docker         | Ejecución aislada de los servicios            |
| Docker Compose | Orquestación de la base de datos y el backend |
| Git            | Control de versiones                          |

---

## Arquitectura del proyecto

La aplicación sigue una arquitectura de tres capas con comunicación unidireccional:

- **React + Vite** —SPA\*\* — Presenta la interfaz, gestiona el estado de sesión y las rutas. No accede nunca directamente a la base de datos.
- **FastAPI** —Expone la API REST, valida las peticiones, aplica las reglas de negocio y devuelve respuestas normalizadas.
- **PostgreSQL** —Almacena la información de forma persistente.

**Docker y Docker Compose** forman el entorno de desarrollo: PostgreSQL y el backend se ejecutan en contenedores, mientras que el frontend se ejecuta en el host mediante pnpm.

## Estructura del proyecto

```
chambeapp/
├── backend/
│   ├── main.py                     Punto de entrada de FastAPI
│   ├── requirements.txt            Dependencias de Python
│   ├── Dockerfile.dev              Imagen de desarrollo del backend
│   ├── .env                        Variables de entorno del backend
│   ├── application/
│   │   ├── interfaces/             Contratos
│   │   └── use_cases/
│   │       ├── auth/               Registro, login, verificación, reset
│   │       └── users/              Perfil, contraseña, consulta
│   ├── domain/
│   │   ├── entities/               Modelos de dominio y enumeraciones
│   │   ├── exceptions/             Excepciones propias del negocio
│   │   ├── repositories/           Interfaces de repositorio
│   │   └── utils/                  Constantes
│   └── infrastructure/
│       ├── api/
│       │   ├── dependencies.py     Inyección de dependencias
│       │   └── routers/            Routers
│       ├── db/
│       │   ├── database.py         Motor y sesión de SQLAlchemy
│       │   └── models/             Modelos de tabla
│       ├── mappers/               Conversión entidad ↔ DTO
│       ├── repositories/          Implementaciones de repositorio
│       ├── schemas/               Esquemas Pydantic de entrada y salida
│       ├── security/              JWT y hash de contraseñas
│       └── services/              Servicio de correo
│
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   ├── components.json             Configuración de shadcn/ui
│   ├── index.html
│   ├── .env                        Variables de entorno del frontend
│   ├── public/
│   └── src/
│       ├── main.tsx                Punto de entrada de React
│       ├── App.tsx                 Definición de rutas
│       ├── assets/
│       ├── components/ui/          Componentes reutilizables
│       ├── context/                Contexto de autenticación
│       ├── hooks/                  Hooks personalizados
│       ├── interfaces/             Tipos de datos de la API
│       ├── lib/                    Utilidades
│       ├── pages/
│       │   ├── auth/               Login, registro, verificación, reset
│       │   ├── dashboard/          Resumen general
│       │   ├── layout/             Layouts, rutas protegidas, navbar, sidebar
│       │   ├── projects/           Reservado
│       │   └── tasks/              Reservado
│       └── services/               Cliente HTTP y servicios de auth
│
├── docker-compose.yml
└── README.md
```

---

## Requisitos previos

| Herramienta    | Versión mínima    | Necesaria para                       |
| -------------- | ----------------- | ------------------------------------ |
| Docker         | [TO BE COMPLETED] | Base de datos y backend              |
| Docker Compose | [TO BE COMPLETED] | Orquestación de contenedores         |
| Git            | [TO BE COMPLETED] | Clonar el repositorio                |
| Node.js        | [TO BE COMPLETED] | Frontend                             |
| pnpm           | [TO BE COMPLETED] | Gestión de dependencias del frontend |

---

## Instalación y configuración

### 1. Clonar el repositorio

```bash
git clone git@github.com:JosePucMoo/Chambeapp.git
cd Chambeapp
```

### 2. Configurar las variables de entorno

Crea manualmente el archivo de entorno del backend:

```bash
touch backend/.env
```

Y el archivo de entorno del frontend:

```bash
touch frontend/.env
```

Completa sus valores siguiendo la sección [Variables de entorno](#variables-de-entorno).

### 3. Levantar los contenedores

```bash
docker compose up -d
```

Esto inicia **PostgreSQL** y el **backend**. Las tablas se crean automáticamente en el primer arranque.

### 4. Instalar las dependencias del frontend

```bash
cd frontend
pnpm install
```

### 5. Iniciar el frontend

```bash
pnpm dev
```

### 6. Acceder a la aplicación

| Servicio                | URL                                  |
| ----------------------- | ------------------------------------ |
| Frontend                | `http://localhost:5173`              |
| Documentación de la API | `http://localhost:8000/docs`         |
| Esquema OpenAPI         | `http://localhost:8000/openapi.json` |
| PostgreSQL              | `localhost:5432`                     |
| Depuración (debugpy)    | `localhost:5678`                     |

---

## Variables de entorno

### Backend — `backend/.env`

Ejemplo:

```env
POSTGRES_USER=admin
POSTGRES_PASSWORD=secretpassword
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_NAME=chambeapp_db
SECRET_KEY=[TO BE COMPLETED]
MAILTRAP_USER=[TO BE COMPLETED]
MAILTRAP_PASS=[TO BE COMPLETED]
MAILTRAP_HOST[TO BE COMPLETED]
MAILTRAP_PORT=[TO BE COMPLETED]
FRONTEND_URL=http://localhost:5173
```

### Frontend — `frontend/.env`

Ejemplo:

```env
VITE_CHAMBEAPP_API_ORIGIN=http://localhost:8000
```

---

## Desarrollo

### Frontend

```bash
cd frontend
pnpm install          # Instalar dependencias
pnpm dev              # Servidor de desarrollo con HMR
pnpm build            # Comprobación de tipos y build de producción
pnpm lint             # Análisis estático con ESLint
pnpm preview          # Previsualizar el build de producción
```

### Backend

```bash
# Ejecutar dentro del contenedor
docker compose logs -f backend

# Ejecución nativa
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Depuración remota
python -m debugpy --listen 0.0.0.0:5678 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Pruebas

[TO BE COMPLETED] — El proyecto no incluye actualmente un framework de pruebas ni una suite de tests automatizados.

## Autor

José Puc
