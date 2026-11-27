-- Participant modul – schema.sql
-- Defines the database schema for the Participant module.
-- Loaded automatically by Docker on first startup via docker-entrypoint-initdb.d.
-- This module stores personal data and should have restricted access.

-- 1. Participants table
-- Each participant is identified by a unique pseudonym shared across all three modules.
-- A participant is registered automatically on their first demographic data collection.
CREATE TABLE participants (
    participant_pseudonym VARCHAR(225) PRIMARY KEY,  -- Unique identifier shared across modules
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- 2. API keys table
-- Used to authenticate requests from other modules (e.g. the Experiment module).
-- Keys are stored as hashes, never in plain text.
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,       -- Human-readable name for the key
    key_hash VARCHAR(255) NOT NULL,   -- Hashed API key, never stored in plain text
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- 3. Demographic data table
-- Each row represents one demographic data collection for one participant in one session.
-- A participant can have multiple records, one per experiment run.
-- age, sex, occupation and major are filled in by the participant via the display_url form.
CREATE TABLE demographics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    participant_pseudonym VARCHAR(255) NOT NULL REFERENCES participants(participant_pseudonym),
    session_ref VARCHAR(255) NOT NULL,   -- The Experiment module's session ID
    group_ref VARCHAR(255) NOT NULL,     -- The ethics approval number; used to filter by experiment
    language VARCHAR(5) NOT NULL CHECK(language IN ('en', 'hu')),
    status VARCHAR(20) NOT NULL DEFAULT 'in_progress' CHECK (status IN ('in_progress', 'completed')),
    age INTEGER,                         -- NULL until the participant completes the form
    sex VARCHAR(1) CHECK (sex IN ('m', 'f')),
    occupation VARCHAR(255),
    major VARCHAR(255),
    started_at TIMESTAMP NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMP DEFAULT NULL, -- Set when the participant submits the form
    api_key_id UUID REFERENCES api_keys(id)  -- Tracks which API key started this collection
);

-- Index on group_ref for fast filtering by ethics approval number
CREATE INDEX idx_demographics_group_ref ON demographics(group_ref);