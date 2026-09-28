-- Creates the application database and role for a manual (non-Docker) install.
--
--   psql -U postgres -f setup_db.sql
--
-- Docker Compose does not need this: the `db` service creates both from
-- POSTGRES_DB / POSTGRES_USER on first start.
--
-- Guarded with \gexec so the script is safe to re-run.

SELECT 'CREATE ROLE abiturend LOGIN PASSWORD ''abiturend'''
WHERE NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'abiturend')\gexec

SELECT 'CREATE DATABASE abiturend OWNER abiturend'
WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'abiturend')\gexec
