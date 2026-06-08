-- =============================================================================
-- Golden Horizon AI - PostgreSQL initialisation
-- Runs once automatically on first container start (empty data volume).
-- Phase 1: extensions only. Table schema + migrations land in Phase 2.
-- =============================================================================

-- Vector similarity search for the knowledge base / semantic search.
CREATE EXTENSION IF NOT EXISTS vector;

-- UUID generation + crypto helpers.
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Sanity check row so you can confirm init ran:
--   docker/podman exec -it gh_postgres psql -U $POSTGRES_USER -d $POSTGRES_DB -c "SELECT extname FROM pg_extension;"
