CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE OR REPLACE FUNCTION generate_searchable(_name VARCHAR, _email VARCHAR)
    RETURNS TEXT AS
$$
BEGIN
    RETURN _name || _email;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE TABLE IF NOT EXISTS users
(
    id         UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name       VARCHAR(50) NOT NULL,
    email      VARCHAR(50) UNIQUE,
    searchable TEXT GENERATED ALWAYS AS (generate_searchable(name, email) ) STORED
);

CREATE INDEX IF NOT EXISTS search_user_index ON users USING GIST (searchable gist_trgm_ops);