PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS runtime_schema (
    version INTEGER NOT NULL
);

INSERT INTO runtime_schema(version)
SELECT 4 WHERE NOT EXISTS (SELECT 1 FROM runtime_schema);

CREATE TABLE IF NOT EXISTS jobs (
    job_id TEXT PRIMARY KEY,
    idempotency_key TEXT NOT NULL UNIQUE,
    source TEXT NOT NULL,
    source_event_id TEXT NOT NULL,
    intent TEXT NOT NULL,
    payload_ref TEXT NOT NULL,
    original_path TEXT NOT NULL,
    source_device INTEGER,
    source_inode INTEGER,
    source_size INTEGER,
    source_mtime_ns INTEGER,
    lane TEXT NOT NULL,
    policy_profile TEXT NOT NULL,
    priority INTEGER NOT NULL,
    not_before REAL,
    requested_capability TEXT,
    state TEXT NOT NULL,
    capability TEXT,
    skill_digest TEXT,
    plan_hash TEXT,
    execution_generation INTEGER NOT NULL DEFAULT 1,
    lease_owner TEXT,
    lease_generation INTEGER NOT NULL DEFAULT 0,
    lease_expires_at REAL,
    attempts INTEGER NOT NULL DEFAULT 0,
    commit_attempts INTEGER NOT NULL DEFAULT 0,
    cancel_requested INTEGER NOT NULL DEFAULT 0,
    last_error TEXT,
    result_path TEXT,
    supersedes_job_id TEXT REFERENCES jobs(job_id),
    created_at REAL NOT NULL,
    updated_at REAL NOT NULL
);

CREATE INDEX IF NOT EXISTS jobs_claimable
ON jobs(state, not_before, priority DESC, created_at);

CREATE TABLE IF NOT EXISTS job_events (
    job_id TEXT NOT NULL REFERENCES jobs(job_id) ON DELETE CASCADE,
    sequence INTEGER NOT NULL,
    event_type TEXT NOT NULL,
    at REAL NOT NULL,
    detail_json TEXT NOT NULL,
    PRIMARY KEY(job_id, sequence)
);

CREATE TABLE IF NOT EXISTS tool_calls (
    call_id TEXT PRIMARY KEY,
    job_id TEXT NOT NULL REFERENCES jobs(job_id) ON DELETE CASCADE,
    tool_name TEXT NOT NULL,
    arguments_json TEXT NOT NULL,
    result_hash TEXT,
    policy_decision TEXT NOT NULL,
    duration_ms REAL NOT NULL,
    error TEXT,
    created_at REAL NOT NULL
);
