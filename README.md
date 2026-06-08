# Golden Horizon AI Backend

AI infrastructure for Golden Horizon. This repository is **the AI backend, not the website**. The WordPress/WooCommerce store lives separately and talks to this backend through REST APIs and webhooks.

The backend is the **source of truth**. OpenClaw and Claude never talk to WooCommerce directly — everything routes through this backend.

- **Repo:** https://github.com/steven89-rgb/golden-horizon-ai
- **Dev:** local machine
- **Deploy target:** Rocky Linux 8 VPS running **Podman**

## Stack

- **Backend:** Python 3.12, FastAPI
- **Database:** PostgreSQL 16 + pgvector
- **Agent layer:** OpenClaw (added in a later phase)
- **Automation:** N8N
- **Containers:** Podman / Docker compatible (`compose.yaml`)

## Project structure

```
backend/          FastAPI application
  api/            API routers (health, plus more in later phases)
  main.py         App entrypoint
  requirements.txt
database/         DB bootstrap + migrations
  init.sql        Extensions (pgvector, pgcrypto); schema lands in Phase 2
docker/           Container build files
  backend.Dockerfile
openclaw/         Agent layer (Phase 7)
n8n/              Workflow definitions (Phase 9)
docs/             Documentation
compose.yaml      Container stack (Podman/Docker compatible)
.env.example      Environment template
```

## Quick start (local development)

Requires Podman + podman-compose, or Docker + Docker Compose.

```bash
# 1. Configure environment
cp .env.example .env
# edit .env and set POSTGRES_PASSWORD, N8N_ENCRYPTION_KEY, etc.
openssl rand -hex 24   # value for N8N_ENCRYPTION_KEY

# 2. Build and start
podman compose up --build        # or: docker compose up --build

# 3. Verify
curl http://localhost:8000/health        # {"status":"ok",...}
curl http://localhost:8000/health/ready  # {"status":"ready"}
# n8n UI: http://localhost:5678  (basic auth)
```

### Run the API without containers

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```

## Services (`compose.yaml`)

| Service    | Host port | Notes                                            |
|------------|-----------|--------------------------------------------------|
| `postgres` | none      | pgvector; internal network only, **not published** |
| `backend`  | 8000      | FastAPI                                           |
| `n8n`      | 5678      | Automation, persists to Postgres, basic auth     |
| `openclaw` | none      | Internal only; enabled in a later phase          |

Postgres has no host port by design. For admin access on the VPS:

```bash
podman exec -it gh_postgres psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"
```

## Deploying to the Rocky Linux 8 VPS

```bash
sudo dnf install -y podman podman-compose git
git clone https://github.com/steven89-rgb/golden-horizon-ai.git
cd golden-horizon-ai
cp .env.example .env && chmod 600 .env   # set real secrets
podman compose up -d --build
```

Open only the ports you actually serve in `firewalld` (e.g. the reverse proxy / API). Keep 5432 closed.

## Roadmap

**Phase 1 (this delivery):** project skeleton, container stack, health endpoints, DB extension bootstrap.

**Next — Phase 2:** PostgreSQL schema and Alembic migrations.
