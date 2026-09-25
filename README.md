# Chambeapp

Project and task management web application with a Kanban-type system. It allows you to organize projects, create and manage tasks, and view the status of work by columns.

## Technologies

- **Frontend:** React, Vite, TypeScript, React Router, Tailwind CSS, shadcn/ui, Axios
- **Backend:** Python, FastAPI, Uvicorn, SQLAlchemy, Pydantic, PyJWT
- **Database:** PostgreSQL
- **Containers:** Docker, Docker Compose

## Prerequisites

- Docker
- Docker Compose
  -Git
- Node.js and pnpm (to run the frontend locally)

## Environment variables

**Backend — `backend/.env`**

```send
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_NAME=

SECRET_KEY=

MAILTRAP_USER=
MAILTRAP_PASS=
MAILTRAP_HOST=sandbox.smtp.mailtrap.io
MAILTRAP_PORT=2525

FRONTEND_URL=http://localhost:5173
```

**Frontend — `frontend/.env`**

```send
VITE_CHAMBEAPP_API_ORIGIN=http://localhost:8000
```

| Variable                    | Description   |
| --------------------------- | ------------- |
| `VITE_CHAMBEAPP_API_ORIGIN` | API base URL. |

## Backend installation

1. Create the virtual environment and install the dependencies:

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Create the `backend/.env` file with the values described above.

3. Start the API:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The service is available at `http://localhost:8000` and the tables are created automatically on first boot.

## Frontend installation

```bash
cd frontend
pnpm install
pnpm dev
```

The Vite server is available at `http://localhost:5173`.

## Running with Docker Compose

The `docker-compose.yml` file defines two services: `db` (PostgreSQL) and `backend` (FastAPI). The frontend is not part of Compose and runs locally.

```bash
docker compose up -d
```

With this, PostgreSQL remains on port `5432` and the API on `8000`. To also get the frontend up, run `pnpm dev` in the `frontend` folder.

## Container Commands

```bash
docker compose up -d # Start services
docker compose down # Stop services
docker compose build # Rebuild the images
docker compose up -d --build # Rebuild and restart
docker compose logs -f # View logs
docker compose ps # View the status of services
```

PostgreSQL data is stored in the `postgres_data` volume. The backend code is mounted as a volume, so changes are applied without rebuilding the image. Use `docker compose down -v` to remove the data as well.

## API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI:** `http://localhost:8000/docs`
- **OpenAPI schema:** `http://localhost:8000/openapi.json`
