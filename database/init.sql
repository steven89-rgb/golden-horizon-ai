-- =============================================================================
-- Golden Horizon AI - PostgreSQL initialisation
-- Runs once automatically on first container start (empty data volume).
-- Phase 1: extensions only. Table schema + migrations land in Phase 2.
-- =============================================================================

-- Vector similarity search for the knowledge base / semantic search.
CREATE EXTENSION IF NOT EXISTS vector;

-- UUID generation + crypto helpers.
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create the n8n database (n8n requires its own DB).
-- CREATE DATABASE cannot run inside a transaction block in entrypoint scripts,
-- so we use a DO block with dblink to work around it.
CREATE EXTENSION IF NOT EXISTS dblink;
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'n8n') THEN
    PERFORM dblink_exec('dbname=' || current_database(), 'CREATE DATABASE n8n');
  END IF;
END
$$;

-- Sanity check row so you can confirm init ran:
--   docker/podman exec -it gh_postgres psql -U $POSTGRES_USER -d $POSTGRES_DB -c "SELECT extname FROM pg_extension;"
