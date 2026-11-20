-- Participant modul - schema.sql

-- 1. Résztvevők tábla
CREATE TABLE participants (
    participant_pseudonym VARCHAR(225) PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- 2. API kulcsok
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    key_hash VARCHAR(255) NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- 3. Demográfiai adatok tábla
CREATE TABLE demographics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    participant_pseudonym VARCHAR(255) NOT NULL REFERENCES participants(participant_pseudonym),
    session_ref VARCHAR(255) NOT NULL,
    group_ref VARCHAR(255) NOT NULL,
    language VARCHAR(5) NOT NULL CHECK(language IN ('en', 'hu')),
    status VARCHAR(20) NOT NULL DEFAULT 'in_progress' CHECK (status IN ('in_progress', 'completed')),
    age INTEGER,
    sex VARCHAR(1) CHECK (sex IN ('m', 'f')),
    occupation VARCHAR(255),
    major VARCHAR(255),
    started_at TIMESTAMP NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMP DEFAULT NULL,
    api_key_id UUID REFERENCES api_keys(id)

);

CREATE INDEX idx_demographics_group_ref ON demographics(group_ref);