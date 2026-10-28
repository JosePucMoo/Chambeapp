# Chambeapp

Project and task management web application with a Kanban-type system. It allows you to organize projects, create and manage tasks, and view the status of work by columns.

## Technologies

- **Frontend:** React, Vite, TypeScript, React Router, Tailwind CSS, shadcn/ui, Axios
- **Backend:** Python, FastAPI, Uvicorn, SQLAlchemy, Pydantic, PyJWT
- **Database:** PostgreSQL
- **Tooling:** Ruff (lint + format), ESLint, Prettier, pytest
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
POSTGRES_SSLMODE=disable

SECRET_KEY=

SMTP_HOST=sandbox.smtp.mailtrap.io
SMTP_PORT=2525
SMTP_USER=
SMTP_PASS=
SMTP_FROM=no-reply@chambeapp.com

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

## Backend code quality — Ruff

The backend uses [Ruff](https://docs.astral.sh/ruff/) as linter and formatter.

```bash
cd backend
source venv/bin/activate
pip install -r requirements-dev.txt
```

All commands are run from the `backend/` folder with the virtual environment activated:

```bash
ruff check .          # Lint: report errors
ruff check . --fix    # Lint: apply the automatic fixes
ruff format .         # Format all the source code
ruff format --check . # Check the formatting without modifying files (useful in CI)
```

Recommended workflow before committing:

```bash
ruff check . --fix && ruff format . && ruff check .
```

## Frontend installation

```bash
cd frontend
pnpm install
pnpm dev
```

The Vite server is available at `http://localhost:5173`.

## Frontend code quality — ESLint + Prettier

The frontend uses **ESLint** (with `typescript-eslint`, `eslint-plugin-react-hooks` and
`eslint-plugin-react-refresh`) as linter and **Prettier** as formatter. Both are pinned in the
frontend `devDependencies`, so they are installed with:

```bash
cd frontend
pnpm install
```

The configuration lives in `frontend/eslint.config.js` (flat config), `frontend/.prettierrc.json`
and `frontend/.prettierignore`. `eslint-config-prettier` is the last entry of the ESLint config so
the formatting rules of ESLint are disabled in favor of Prettier.

All commands are run from the `frontend/` folder:

```bash
pnpm lint          # ESLint: report errors and warnings
pnpm format        # Prettier: format all the source code
pnpm format:check  # Prettier: check the formatting without modifying files (useful in CI)
pnpm typecheck     # TypeScript: type-check the project (tsc -b)
pnpm build         # TypeScript check + production build
```

Recommended workflow before committing:

```bash
pnpm lint && pnpm format && pnpm format:check && pnpm build
```

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

## Deployment (Netlify + Render + Supabase)

The app is deployable with free tiers:

## Live demo

- **Frontend:** https://chambe-app.netlify.app
- **API (Swagger):** https://chambeapp.onrender.com/docs

## API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI:** `http://localhost:8000/docs`
- **OpenAPI schema:** `http://localhost:8000/openapi.json`
