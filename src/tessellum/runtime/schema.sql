PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS runtime_schema (
    version INTEGER NOT NULL
);

INSERT INTO runtime_schema(version)
SELECT 5 WHERE NOT EXISTS (SELECT 1 FROM runtime_schema);

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
    -- P1 A1.3: durable links from a job to its accepted plan revision +
    -- active commit capsule (nullable — a job may have no revision yet).
    -- SQLite permits forward FK references at CREATE time; the target-table
    -- existence is only checked at row-operation time.
    accepted_revision_id TEXT REFERENCES plan_revisions(revision_id),
    active_capsule_id TEXT REFERENCES commit_capsules(capsule_id),
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

-- ── P1 A1.1/A1.2: durable revision + capsule tables ─────────────────────────
-- These are the snapshot-pinned knowledge-transaction records. A PlanRevision
-- is the accepted-intent content record (revision_id = the accepted-effect
-- set hash from composer.proposals.plan_revision_hash); a CommitCapsule is a
-- content-addressed artifact bundle for one accepted revision at one base
-- generation. capsule_artifacts is the A1.2-mandated CAS manifest (the plan's
-- "+ a manifest row is fine"). NOT a reuse of supersedes_job_id (that is the
-- RETRY-lineage self-FK for dead-lettered/cancelled jobs — a distinct concern).

CREATE TABLE IF NOT EXISTS plan_revisions (
    revision_id TEXT PRIMARY KEY,
    -- parent_revision_id is a content-identity POINTER to the revision this
    -- one was computed against (the merge parent). It is deliberately NOT a
    -- self-FK: a genesis revision's parent is an empty/baseline hash that is
    -- never itself a recorded row (see the accepted plan's deliverable-2 test,
    -- which records rev against an unrecorded genesis parent). Enforcing a
    -- self-FK would break that first-revision case; the pointer only needs to
    -- round-trip byte-identically. Nullable for a rootless revision.
    parent_revision_id TEXT,
    canonical_bytes BLOB NOT NULL,
    decision TEXT NOT NULL,
    evidence TEXT NOT NULL,
    created_at REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS commit_capsules (
    capsule_id TEXT PRIMARY KEY,
    revision_id TEXT NOT NULL REFERENCES plan_revisions(revision_id),
    base_generation INTEGER NOT NULL,
    state TEXT NOT NULL,
    artifact_root TEXT NOT NULL,
    created_at REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS commit_capsules_by_revision
ON commit_capsules(revision_id);

CREATE TABLE IF NOT EXISTS capsule_artifacts (
    capsule_id TEXT NOT NULL REFERENCES commit_capsules(capsule_id) ON DELETE CASCADE,
    artifact_class TEXT NOT NULL,
    address TEXT NOT NULL,
    size INTEGER NOT NULL,
    created_at REAL NOT NULL,
    -- (capsule_id, artifact_class, address): two DISTINCT classes that happen
    -- to share byte-identical content each keep their own manifest row (the
    -- blob CAS still dedups by address on disk). PK on (capsule_id, address)
    -- alone would silently collapse the class->content association.
    PRIMARY KEY (capsule_id, artifact_class, address)
);
CREATE INDEX IF NOT EXISTS capsule_artifacts_by_capsule
ON capsule_artifacts(capsule_id);
