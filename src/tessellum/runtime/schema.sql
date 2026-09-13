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

-- ── The append-only claim/edge log (T1, of-record) ──────────────────────────
-- The episodic epistemic log of the query-time protocol. It is a totally
-- ordered, APPEND-ONLY sequence of claims and operator edges: nothing here is
-- ever rewritten or removed. The argument graph is exactly the FOLD of this
-- log, and the epistemic labelling (proposed / challenged / warranted /
-- superseded) is COMPUTED from that fold on demand -- never stored here as
-- truth. Written only through tessellum.runtime.claim_log, which appends under
-- the same BEGIN IMMEDIATE single-writer transaction as the job queue, and
-- mirrors job_events' discipline (an immutable row per act, ordered by a
-- monotonic position).
--
-- Deliberate divergences from the reference log schema this ports, recorded
-- here so the difference is never rediscovered by reading code:
--   * created_at is REAL epoch seconds, matching job_events.at and every other
--     runtime table, rather than ISO TEXT.
--   * seq is ONE shared log position across claims AND edges (the reference
--     numbers each table independently). The fold needs a total order over the
--     whole log: "this support was re-asserted AFTER the revise" is not
--     expressible in two independent sequences.
--   * derivation_id is a new column -- the deterministic identity of a
--     derivation, hash(note_id, span_locator), which a revision PRESERVES while
--     text_hash changes. claim_id, the log's content address, is
--     hash(derivation_id, text_hash), so a revision is a distinct row.
--   * edges.src / edges.dst carry a foreign key into claims. No edge may name a
--     claim the log does not hold, which is the storage half of the invariant
--     that the folded graph contains no edge without a log record.
-- The schema version stays 5: these are new tables created idempotently by the
-- same executescript, with no column added to an existing table, so there is no
-- migration step to gate. The same holds for the Tier-A and Tier-B sections
-- below.

-- One row per claim: a declarative sentence that can be true or false, plus a
-- locator pointing at where it lives. Claims are OPAQUE TEXT + locator -- no
-- logical form, no triples. A domain relation ("X is owned by Y") is a claim,
-- never an edge; op below is the only relation vocabulary in the system.
--
-- provenance matters because CONSTRUCTING a claim is a reasoning act, not a
-- string extraction, and the difference has to be visible in the data:
--   'stub'        -- located mechanically (a heading, a claim-section
--                    sentence). A PLACEHOLDER: for many notes the heading is a
--                    topic rather than a proposition, and a note asserting
--                    several things collapses into one stub. Any status
--                    computed over a stub is provisional, so the default is the
--                    conservative value.
--   'constructed' -- the proposition stated after READING the source, with a
--                    span locator.
-- source_note_hash binds the claim to the cited note's content at derivation
-- time, so a later vault edit is detectable (the staleness flag P6 appends).
CREATE TABLE IF NOT EXISTS claims (
    claim_id TEXT PRIMARY KEY,
    derivation_id TEXT NOT NULL,
    text TEXT NOT NULL,
    note_id TEXT NOT NULL,
    locator TEXT,
    provenance TEXT NOT NULL DEFAULT 'stub'
        CHECK (provenance IN ('stub', 'constructed')),
    source_note_hash TEXT,
    text_hash TEXT NOT NULL,
    seq INTEGER NOT NULL UNIQUE,
    created_at REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS claims_by_derivation ON claims(derivation_id);
CREATE INDEX IF NOT EXISTS claims_by_note ON claims(note_id);

-- One row per operator edge. op is the ONLY fixed relation vocabulary: exactly
-- four operators, all epistemic. Domain semantics never appears here. origin
-- records HOW the act arose ('projected' from authored structure, 'query'
-- verified at read time, 'reasserted' / 'carried' for the two consequences a
-- revise must log explicitly rather than inherit silently).
CREATE TABLE IF NOT EXISTS edges (
    edge_id TEXT PRIMARY KEY,
    op TEXT NOT NULL
        CHECK (op IN ('support', 'attack', 'revise', 'supersede')),
    src TEXT NOT NULL REFERENCES claims(claim_id),
    dst TEXT NOT NULL REFERENCES claims(claim_id),
    evidence_locator TEXT,
    origin TEXT NOT NULL,
    seq INTEGER NOT NULL UNIQUE,
    created_at REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS edges_by_dst ON edges(dst, op);
CREATE INDEX IF NOT EXISTS edges_by_src ON edges(src, op);

-- Derived-state cache ONLY, never a source of truth: the computed labelling
-- keyed by a digest of the edge set it was computed over, so an append yields a
-- new key and the stale entry is simply never read again. A status is a pure
-- function of the edge set; if it cannot be recomputed from the log it is not a
-- status.
CREATE TABLE IF NOT EXISTS status_cache (
    edgeset_digest TEXT NOT NULL,
    claim_id TEXT NOT NULL REFERENCES claims(claim_id),
    status TEXT NOT NULL,
    PRIMARY KEY (edgeset_digest, claim_id)
);

-- ── Tier A: the resolution hot set -- ONE definition, TWO databases ──────────
-- This section is applied both here (the runtime database) and, through
-- tessellum.runtime.schema.schema_section, to the REGISTRY SIDECAR database,
-- whose lifetime is "rebuild whenever the vault changes" rather than the
-- queue's "durable across restarts". It used to be written out twice, in
-- runtime/registry_store.py and here, and the two copies had already drifted:
-- different NOT NULLs and one extra column on one side, with a runtime
-- PRAGMA probe in the Tier-B store existing only to discover which shape it had
-- been handed. Two definitions of one table is a coincidence, not a schema, so
-- the definition lives here once and both consumers apply this section.
--
-- The reconciled shape is the STRICTER of the two. A relation row whose subject,
-- object, origin or evidence is unknown is not a weaker row, it is an unusable
-- one: the cache is read by subject and answers must be citable, so the columns
-- that make it citable are required rather than hopeful.
--
-- A CACHE / PROJECTION, explicitly NOT a traversable typed-edge graph: read BY
-- SUBJECT, never enumerated across pairs, and dropping it costs latency only,
-- never knowledge. That is why a predicate column here does not contradict the
-- untyped authored link graph in the indexer schema -- these are node-attached
-- authored attributes.
--
-- valid_from / valid_to are NOT optional decoration. A role-style relation
-- without a validity interval confidently returns a FORMER holder; the interval
-- plus the superseded_by chain (a row with superseded_by IS NULL is current)
-- is what makes a recency-resolved answer possible. Being a rebuildable
-- projection rather than the append-only log, this table is the one place a
-- projecting rebuild may restate rows; the log above never does.
--
-- origin is the layering column and it is CHECKed for that reason: 'authored'
-- is the O(N) frontmatter seed a reseed rebuilds wholesale, 'resolved' is the
-- query-derived layer that must survive that reseed, and 'extracted' is the
-- middle case. Each writer scopes its delete to its own origin, so a lax column
-- here would let one layer quietly delete another.
-- ##### BEGIN SECTION: tier_a_relations #####
CREATE TABLE IF NOT EXISTS relations (
    relation_id      TEXT PRIMARY KEY,
    subject_id       TEXT NOT NULL,
    predicate        TEXT NOT NULL,
    object_ref       TEXT NOT NULL,
    object_kind      TEXT NOT NULL CHECK (object_kind IN ('entity', 'literal')),
    valid_from       TEXT,
    valid_to         TEXT,
    evidence_note    TEXT NOT NULL,
    evidence_locator TEXT NOT NULL,
    epistemic_status TEXT,
    origin           TEXT NOT NULL CHECK (
        origin IN ('authored', 'extracted', 'resolved')
    ),
    superseded_by    TEXT,
    content_hash     TEXT
);
CREATE INDEX IF NOT EXISTS relations_by_subject ON relations(subject_id, predicate);
CREATE INDEX IF NOT EXISTS relations_by_origin ON relations(origin);
-- ##### END SECTION: tier_a_relations #####

-- ── Tier B: the query cache and the feedback log behind it ───────────────────
-- Tier B is query->note memory WITH a feedback signal. It exists because the
-- reliability gate a consolidation batch turns on -- eta = (n_pass + 1) /
-- (n_trial + 2), plus "no open correction flag" -- has no data source anywhere
-- else: the append-only claim/edge log records claims, edges and locators, and
-- never whether an answer turned out to be right.
--
-- Both tables are REBUILDABLE PROJECTIONS and both are evictable. query_cache is
-- a projection of derivations that already happened; feedback is a projection of
-- a deployment's own review stream, re-ingestible because every event is content
-- addressed. Dropping either costs latency and precision, never knowledge --
-- which is exactly why row updates and row deletes are legitimate in
-- tessellum.runtime.query_cache and forbidden in tessellum.runtime.claim_log.
--
-- Sectioned for the same reason Tier A is: QueryCacheStore may be opened on this
-- database or on the registry sidecar, and it applies these two tables alone.
-- ##### BEGIN SECTION: tier_b_query_cache #####
-- One row per cached query->notes mapping. feedback_score is STANDING, not
-- truth: a demotable number that a negative verdict lowers and, at the floor,
-- evicts. hits / last_used are eviction inputs and the coverage denominator,
-- never evidence of correctness -- a mapping used a hundred times with no
-- verdict has learned nothing. query_embedding is retained for a later near-miss
-- lookup and is deliberately NOT part of the key: keying on it would make a
-- cache hit depend on a model's opinion of similarity.
CREATE TABLE IF NOT EXISTS query_cache (
    query_key       TEXT PRIMARY KEY,
    query_embedding BLOB,
    target_note_ids TEXT NOT NULL,
    feedback_score  REAL NOT NULL DEFAULT 1.0,
    hits            INTEGER NOT NULL DEFAULT 0,
    last_used       REAL,
    created_at      REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS query_cache_by_standing
ON query_cache(feedback_score, last_used);

-- The feedback log: one immutable row per recorded outcome. Four kinds, and the
-- split between the first two is what makes feedback COVERAGE measurable rather
-- than invisible:
--   'trial'               -- an episode USED the subject (a cached mapping or a
--                            promoted claim). Not yet evidence either way.
--   'verdict'             -- how that episode turned out. n_trial counts these
--                            (adjudicated trials); an unjudged use is counted
--                            separately, never as a failure.
--   'correction_raise'    -- somebody reported this subject as wrong. The gate
--                            condition "no open correction flag" reads these.
--   'correction_release'  -- closes one raised flag, naming it in `releases`.
-- A flag is therefore real state with a lifecycle, not a boolean somebody can
-- flip back without leaving a trace.
--
-- No foreign key to query_cache, deliberately: evicting a mapping must not
-- delete the evidence about it (eviction would otherwise erase exactly the
-- history that justified it), and a 'promoted_claim' subject lives in the claim
-- log, not here. seq is the append position; a repeated verdict for one episode
-- cannot inflate a count because the tally keeps the LAST verdict per episode.
CREATE TABLE IF NOT EXISTS feedback (
    feedback_id  TEXT PRIMARY KEY,
    kind         TEXT NOT NULL CHECK (
        kind IN ('trial', 'verdict', 'correction_raise', 'correction_release')
    ),
    subject_id   TEXT NOT NULL,
    subject_kind TEXT NOT NULL CHECK (
        subject_kind IN ('cached_mapping', 'promoted_claim')
    ),
    episode_id   TEXT NOT NULL,
    verdict      TEXT CHECK (
        verdict IS NULL OR verdict IN ('correct', 'incorrect', 'partial', 'unknown')
    ),
    source       TEXT NOT NULL,
    detail       TEXT NOT NULL DEFAULT '',
    releases     TEXT,
    at           REAL NOT NULL,
    seq          INTEGER NOT NULL UNIQUE,
    -- kind and payload must agree, mirroring FeedbackEvent's own validation: a
    -- verdict row carries a verdict and nothing else does; only a release names
    -- the flag it closes.
    CHECK ((kind = 'verdict') = (verdict IS NOT NULL)),
    CHECK ((kind = 'correction_release') = (releases IS NOT NULL))
);
CREATE INDEX IF NOT EXISTS feedback_by_subject ON feedback(subject_id, kind);
CREATE INDEX IF NOT EXISTS feedback_by_episode ON feedback(episode_id);
-- ##### END SECTION: tier_b_query_cache #####
