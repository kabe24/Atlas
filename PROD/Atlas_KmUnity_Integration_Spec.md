# Atlas-to-KmUnity Integration Spec

**Author:** Claude (AI) + Kalib
**Date:** April 4, 2026
**Last Updated:** April 5, 2026
**Status:** Phases A, C, D, E complete. Phase B partially complete.
**Depends on:** KmUnity Phase 1 (complete), Atlas v1.4.0 (complete)

---

## 1. Goal

Integrate Atlas (AI Tutor) into the KmUnity platform so that:

1. Users access Atlas from the KmUnity portal — same sidebar, same dashboard, same auth
2. Cloud tunnels are eliminated — Atlas's Python backend deploys to Railway
3. KmUnity's Supabase DB tracks session types and token usage for all tools (Atlas, Maven, Soar)
4. KmUnity's content safety middleware (crisis detection, PII stripping, teen safety prompts) covers Atlas AI calls
5. Atlas standalone development continues uninterrupted — new features are built against the Python backend as usual
6. A new **Parent Hub** section provides a centralized home for parent-facing data across all tools

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                    KmUnity Frontend                  │
│               (React + Vite on Railway)              │
│                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │  Maven   │  │   Soar   │  │  Atlas   │  (tools)  │
│  │  (React) │  │  (React) │  │ (iframe) │           │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘           │
│       │              │             │                  │
│  ┌────▼──────────────▼─────────────▼──────────────┐  │
│  │           KmUnity Express Server               │  │
│  │         (port 3000 on Railway)                  │  │
│  │                                                 │  │
│  │  /api/chat ──────── Anthropic (Maven/Soar)      │  │
│  │  /api/atlas/* ──┐   logApiCall() on all paths   │  │
│  │                 │   safety middleware on all     │  │
│  └─────────────────┼───────────────────────────────┘  │
│                    │                                   │
│       ┌────────────▼────────────┐                     │
│       │   Atlas Python Backend  │                     │
│       │  (Railway internal svc) │                     │
│       │   FastAPI / uvicorn     │                     │
│       │   Storage: Supabase     │                     │
│       └────────────┬────────────┘                     │
│                    │                                   │
│       ┌────────────▼────────────┐                     │
│       │       Supabase          │                     │
│       │  profiles, families,    │                     │
│       │  atlas_profiles,        │                     │
│       │  atlas_diagnostics,     │                     │
│       │  atlas_practice,        │                     │
│       │  api_calls, sessions    │                     │
│       └─────────────────────────┘                     │
└─────────────────────────────────────────────────────┘
```

### Key architectural decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Atlas backend language | **Keep Python** | 65 features of battle-tested learning engine logic. Rewriting in Node adds risk with zero functional gain. |
| Atlas frontend approach | **iframe (Phase 1), React (Phase 2)** | iframe lets us ship fast with minimal UX disruption. React rebuild can happen incrementally per-screen. |
| Data storage | **Migrate to Supabase** | Small user base now — rip the band-aid off. Avoids throwaway mapping layer. |
| Storage abstraction | **Yes — dual backend** | Python code gets a `StorageBackend` interface with `FileStorage` (dev) and `SupabaseStorage` (prod) implementations. Standalone dev workflow preserved. |
| Parent experience | **Parent Hub (sidebar section)** | Dedicated section at same level as Tools and Account. Not buried in Settings. Supports future per-tool parent views. |
| Safety middleware | **Proxy-level enforcement** | Atlas AI calls route through Express, which applies the same crisis detection, PII stripping, and content filtering as Maven/Soar. |
| Deployment | **Railway multi-service** | Atlas Python runs as a second Railway service in the same project. Express proxies to it via internal networking. |

---

## 3. Sidebar Navigation Restructure

Current sidebar:
```
Dashboard
── Tools ──
  Maven
  Soar
── Account ──
  Family
  Settings
```

New sidebar:
```
Dashboard
── Tools ──
  Maven
  Soar
  Atlas
── Parent Hub ──          ← NEW section, only visible to parent profiles
  Overview                ← Cross-tool summary (sessions, safety alerts, usage)
  Atlas Progress          ← Atlas parent portal (proficiency, focus, action plan)
  [Maven Insights]        ← Future: interview scores, resume progress
  [Soar Insights]         ← Future: module completion, lab scores
── Account ──
  Family
  Settings
```

**Visibility rules:**
- `Parent Hub` section is visible only when `profile.profile_type === 'parent'`
- Teen profiles see Tools + Account (no Parent Hub)
- Child profiles see Tools only (simplified dashboard)
- The Atlas tool tile on Dashboard links to `/tools/atlas` (student experience)

---

## 4. Work Breakdown

### Phase A: Foundation (Railway + Storage Abstraction)
*Estimated effort: 3-4 days*

| Task | Details |
|------|---------|
| A-01: Deploy Atlas Python backend to Railway | Create a second Railway service in the KmUnity project. Dockerfile with Python 3.11, uvicorn, FastAPI. Internal networking only (no public URL). |
| A-02: Express proxy routes | Add `/api/atlas/*` proxy in `server/index.js`. Forward requests to Atlas Python service. Pass auth headers through. |
| A-03: Storage abstraction layer | Create `storage_backend.py` with `StorageBackend` base class. Implement `FileStorage` (current behavior) and `SupabaseStorage`. Switch via `STORAGE_BACKEND` env var. |
| A-04: Supabase tables for Atlas | Migration 007: `atlas_profiles`, `atlas_diagnostics`, `atlas_practice_history`, `atlas_mastery`. See schema in Section 5. |
| A-05: Auth bridge middleware | Express middleware that resolves KmUnity profile → Atlas instance_id + student_id. Sets headers on proxied requests so Atlas Python knows who's calling. |
| A-06: Environment config | Atlas Python reads `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `STORAGE_BACKEND`, `ANTHROPIC_API_KEY` from Railway env vars. |

### Phase B: Platform Integration (API Calls + Safety + Tool Registration)
*Estimated effort: 2-3 days*

| Task | Details |
|------|---------|
| B-01: Token tracking on Atlas AI calls | Express proxy intercepts Atlas responses that include token usage metadata. Calls `logApiCall()` with `tool: 'atlas'`, module (diagnostic/practice/tutor), model, tokens, cost. |
| B-02: Safety middleware for Atlas | Route Atlas AI calls through `detectCrisisSignals()`, `stripPII()`, `filterContent()`, and `appendTeenSafety()`. Atlas Python returns raw AI text; Express applies safety filters before sending to client. |
| B-03: Activate Atlas in tools registry | `UPDATE tools SET is_active = true WHERE slug = 'atlas';` Add Atlas to `TOOLS` array in `ToolShell.jsx`. Add tool card to `Dashboard.jsx`. |
| B-04: Atlas tool access + rate limiting | Add `atlas` to `MODULE_TO_TOOL_SLUG` mapping. Atlas sessions counted against daily limits. Parent tool access controls work for Atlas. |
| B-05: Session tracking | Atlas sessions create rows in the `sessions` table (tool_id = atlas). Session start/end lifecycle matches Maven/Soar pattern. |

### Phase C: Frontend Integration (Student Experience)
*Estimated effort: 3-4 days*

| Task | Details |
|------|---------|
| C-01: AtlasLayout component | React component at `/tools/atlas`. Renders Atlas header + navigation (My Map, Practice, Explore, Diagnostics). Uses iframe pointing to Atlas's static HTML initially. |
| C-02: Auth handoff to iframe | Pass KmUnity auth token + profile ID to Atlas iframe via `postMessage`. Atlas Python validates and maps to internal student identity. |
| C-03: Atlas dashboard tile | Add Atlas card to Dashboard with `AtlasMark` SVG, gradient (`#6366F1→#818CF8`), and coming-soon / active state based on `tools.is_active`. |
| C-04: Tool disclaimer | Add Atlas to `ToolDisclaimer` component: "Atlas is an AI tutor, not a licensed teacher. It provides educational support but cannot replace classroom instruction." (Already defined in KmUnity Features Spec S-02.) |
| C-05: Mobile responsive | Atlas iframe responsive within ToolShell. Mobile hamburger menu works with Atlas as a tool. |

### Phase D: Parent Hub
*Estimated effort: 3-4 days*

| Task | Details |
|------|---------|
| D-01: Parent Hub sidebar section | Add `Parent Hub` nav section to `ToolShell.jsx` between Tools and Account. Conditionally rendered for parent profiles only. |
| D-02: Parent Hub Overview page | `/parent-hub` — Cross-tool summary: recent activity per child, safety alerts, usage stats. Pulls from `sessions`, `api_calls`, `notifications` tables. |
| D-03: Atlas Progress page | `/parent-hub/atlas` — Port of Atlas parent.html functionality into React. Proficiency bars, topic drill-down, Focus This Week override, action plan view. Calls Atlas Python APIs via Express proxy. |
| D-04: Notification integration | Atlas activity creates parent notifications via existing `upsertActivitySummary()` and `sendSafetyAlert()` functions. |
| D-05: Focus override API bridge | Parent Hub Atlas Progress page can set Focus This Week via `POST /api/atlas/instance/{id}/student/{id}/focus`. Express proxy forwards to Atlas Python. |

### Phase E: Data Migration & Cutover
*Estimated effort: 1-2 days*

| Task | Details |
|------|---------|
| E-01: Migration script | Python script that reads existing Atlas JSON profiles and writes to Supabase tables. Maps current instance/student names to KmUnity family_id/profile_id. |
| E-02: Profile mapping | For each existing Atlas family: find or create KmUnity family, map parent and student profiles, preserve all diagnostic/practice/mastery data. |
| E-03: Verify data integrity | Compare migrated Supabase data against original JSON files. All proficiency scores, diagnostic results, and practice history must match. |
| E-04: Flip `is_active` in production | Enable Atlas tool in Supabase tools table. Update `STORAGE_BACKEND=supabase` on Railway. |

---

## 5. Supabase Schema — Atlas Tables

```sql
-- Migration 007: Atlas Learning Tool Tables
-- Migrates Atlas's file-based storage to Supabase

BEGIN;

-- ============================================================
-- Atlas student profiles (learning state per subject)
-- One row per student per subject
-- ============================================================
CREATE TABLE IF NOT EXISTS atlas_profiles (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  profile_id      UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  family_id       UUID NOT NULL REFERENCES families(id) ON DELETE CASCADE,
  subject         TEXT NOT NULL,          -- 'math', 'ela', 'science'
  grade           INTEGER,               -- 7, 8, etc.
  topics          JSONB DEFAULT '{}',     -- { "Ratios": { "correct": 5, "total": 8 }, ... }
  proficiency     JSONB DEFAULT '{}',     -- { "Ratios": 0.85, "Geometry": 0.42, ... }
  current_lesson  JSONB DEFAULT '{}',     -- active lesson state
  preferences     JSONB DEFAULT '{}',     -- voice, difficulty, etc.
  created_at      TIMESTAMPTZ DEFAULT now(),
  updated_at      TIMESTAMPTZ DEFAULT now(),
  UNIQUE (profile_id, subject)
);

CREATE INDEX IF NOT EXISTS idx_atlas_profiles_profile ON atlas_profiles(profile_id);
CREATE INDEX IF NOT EXISTS idx_atlas_profiles_family ON atlas_profiles(family_id);

-- ============================================================
-- Diagnostic results
-- ============================================================
CREATE TABLE IF NOT EXISTS atlas_diagnostics (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  profile_id      UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  subject         TEXT NOT NULL,
  grade           INTEGER,
  status          TEXT DEFAULT 'in_progress',   -- 'in_progress', 'complete'
  questions       JSONB DEFAULT '[]',           -- array of question objects
  results         JSONB DEFAULT '{}',           -- { topic: { correct, total, pct } }
  started_at      TIMESTAMPTZ DEFAULT now(),
  completed_at    TIMESTAMPTZ,
  created_at      TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_atlas_diag_profile ON atlas_diagnostics(profile_id, subject);

-- ============================================================
-- Practice history (every practice session)
-- ============================================================
CREATE TABLE IF NOT EXISTS atlas_practice_history (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  profile_id      UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  subject         TEXT NOT NULL,
  topic           TEXT NOT NULL,
  difficulty      TEXT,                   -- 'easy', 'medium', 'hard'
  questions       JSONB DEFAULT '[]',     -- questions + answers
  score           NUMERIC(5,2),           -- percentage
  duration_sec    INTEGER,
  created_at      TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_atlas_practice_profile ON atlas_practice_history(profile_id, subject);
CREATE INDEX IF NOT EXISTS idx_atlas_practice_topic ON atlas_practice_history(topic, created_at);

-- ============================================================
-- Parent focus overrides
-- ============================================================
CREATE TABLE IF NOT EXISTS atlas_focus_overrides (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  profile_id      UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  family_id       UUID NOT NULL REFERENCES families(id) ON DELETE CASCADE,
  subject         TEXT NOT NULL,
  topic           TEXT NOT NULL,
  set_by          UUID NOT NULL REFERENCES profiles(id),   -- parent profile
  expires_at      TIMESTAMPTZ,
  created_at      TIMESTAMPTZ DEFAULT now(),
  UNIQUE (profile_id, subject)
);

-- ============================================================
-- RLS policies
-- ============================================================
ALTER TABLE atlas_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE atlas_diagnostics ENABLE ROW LEVEL SECURITY;
ALTER TABLE atlas_practice_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE atlas_focus_overrides ENABLE ROW LEVEL SECURITY;

-- Students can read/write their own data
CREATE POLICY "Own atlas profile access" ON atlas_profiles
  FOR ALL USING (profile_id = auth.uid())
  WITH CHECK (profile_id = auth.uid());

-- Parents can read their children's data
CREATE POLICY "Parent read family atlas profiles" ON atlas_profiles
  FOR SELECT USING (
    family_id IN (SELECT family_id FROM profiles WHERE id = auth.uid())
  );

-- Same pattern for diagnostics, practice, focus
CREATE POLICY "Own atlas diagnostics" ON atlas_diagnostics
  FOR ALL USING (profile_id = auth.uid())
  WITH CHECK (profile_id = auth.uid());

CREATE POLICY "Parent read family diagnostics" ON atlas_diagnostics
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM profiles child
      WHERE child.id = atlas_diagnostics.profile_id
        AND child.managed_by = auth.uid()
    )
  );

CREATE POLICY "Own atlas practice" ON atlas_practice_history
  FOR ALL USING (profile_id = auth.uid())
  WITH CHECK (profile_id = auth.uid());

CREATE POLICY "Parent read family practice" ON atlas_practice_history
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM profiles child
      WHERE child.id = atlas_practice_history.profile_id
        AND child.managed_by = auth.uid()
    )
  );

-- Focus overrides: parents can set, students can read
CREATE POLICY "Students read own focus" ON atlas_focus_overrides
  FOR SELECT USING (profile_id = auth.uid());

CREATE POLICY "Parents manage family focus" ON atlas_focus_overrides
  FOR ALL USING (
    family_id IN (SELECT family_id FROM profiles WHERE id = auth.uid())
    AND EXISTS (
      SELECT 1 FROM profiles WHERE id = auth.uid() AND profile_type = 'parent'
    )
  );

-- Service role full access (for Python backend via supabaseAdmin)
CREATE POLICY "Service role atlas profiles" ON atlas_profiles
  FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role atlas diagnostics" ON atlas_diagnostics
  FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role atlas practice" ON atlas_practice_history
  FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role atlas focus" ON atlas_focus_overrides
  FOR ALL USING (auth.role() = 'service_role');

COMMIT;
```

---

## 6. Storage Abstraction Layer

The storage abstraction allows Atlas's Python backend to work with either file-based JSON (standalone dev) or Supabase (production) without changing any learning engine logic.

### Interface

```python
# storage_backend.py

class StorageBackend:
    """Abstract interface for Atlas data persistence."""

    def load_profile(self, subject, student_id, instance_id=None):
        raise NotImplementedError

    def save_profile(self, subject, student_id, profile_data, instance_id=None):
        raise NotImplementedError

    def load_diagnostic(self, subject, student_id, instance_id=None):
        raise NotImplementedError

    def save_diagnostic(self, subject, student_id, diagnostic_data, instance_id=None):
        raise NotImplementedError

    def load_practice_history(self, subject, student_id, topic=None, instance_id=None):
        raise NotImplementedError

    def save_practice_result(self, subject, student_id, result, instance_id=None):
        raise NotImplementedError

    def load_focus(self, student_id, instance_id=None):
        raise NotImplementedError

    def save_focus(self, student_id, focus_data, instance_id=None):
        raise NotImplementedError
```

### Implementations

**`FileStorage`** — wraps the current `load_profile()` / `save_profile()` functions. No behavior change. Used when `STORAGE_BACKEND=file` (default for standalone dev).

**`SupabaseStorage`** — reads/writes to the atlas_* Supabase tables using the service role client. Used when `STORAGE_BACKEND=supabase` (production on Railway).

### Initialization

```python
# In app.py startup
import os
from storage_backend import FileStorage, SupabaseStorage

if os.getenv("STORAGE_BACKEND") == "supabase":
    storage = SupabaseStorage(
        url=os.getenv("SUPABASE_URL"),
        key=os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    )
else:
    storage = FileStorage(base_dir="data")
```

All existing `load_profile()` / `save_profile()` calls in `app.py` get replaced with `storage.load_profile()` / `storage.save_profile()`. The function signatures stay the same. The learning engine code doesn't change.

---

## 7. Express Proxy Design

### Route pattern

```javascript
// server/index.js — Atlas proxy section

import { createProxyMiddleware } from 'http-proxy-middleware';

const ATLAS_BACKEND_URL = process.env.ATLAS_BACKEND_URL || 'http://localhost:8000';

// Atlas proxy — forwards /api/atlas/* to Python backend
app.use('/api/atlas', checkRateLimit, atlasAuthBridge, createProxyMiddleware({
  target: ATLAS_BACKEND_URL,
  changeOrigin: true,
  pathRewrite: { '^/api/atlas': '/api' },
  onProxyRes: (proxyRes, req, res) => {
    // Intercept responses to log API calls
    // (token tracking happens here)
  },
}));
```

### Auth bridge middleware

```javascript
// Resolves KmUnity auth → Atlas identity headers
async function atlasAuthBridge(req, res, next) {
  const authHeader = req.headers.authorization;
  if (!authHeader || !supabaseAdmin) return next();

  try {
    const token = authHeader.replace('Bearer ', '');
    const { data: { user } } = await supabaseAdmin.auth.getUser(token);
    if (!user) return next();

    const activeProfileId = req.cookies?.kmu_active_profile || user.id;
    const { data: profile } = await supabaseAdmin
      .from('profiles')
      .select('id, family_id, profile_type, display_name')
      .eq('id', activeProfileId)
      .single();

    if (profile) {
      // Set headers that Atlas Python reads
      req.headers['x-atlas-student-id'] = profile.id;
      req.headers['x-atlas-instance-id'] = profile.family_id;
      req.headers['x-atlas-profile-type'] = profile.profile_type;
      req.headers['x-atlas-display-name'] = profile.display_name;
    }
  } catch (err) {
    console.error('Atlas auth bridge error:', err);
  }
  next();
}
```

### Safety middleware for Atlas AI calls

Atlas AI calls (diagnostic generation, practice questions, tutor conversations) get routed through a dedicated endpoint that applies KmUnity's safety pipeline:

```javascript
app.post('/api/atlas/ai/chat', checkRateLimit, async (req, res) => {
  // 1. Resolve profile (same pattern as /api/chat)
  // 2. appendTeenSafety() to system prompt if teen
  // 3. stripPII() on user messages if teen
  // 4. detectCrisisSignals() on inbound
  // 5. Forward to Atlas Python for AI response
  // 6. detectCrisisSignals() + filterContent() on outbound
  // 7. logApiCall() with tool='atlas', module from request
  // 8. Stream response to client
});
```

---

## 8. Token Tracking Integration

Atlas's Python backend already makes Anthropic API calls for:
- Diagnostic question generation
- Practice question generation
- Tutor conversations (stuck detection)
- AI-powered explanations

Each of these calls returns token usage from the Anthropic SDK. The Python backend includes this in its response metadata:

```python
# In Atlas Python response format
{
  "data": { ... },  # normal response payload
  "_meta": {
    "model": "claude-sonnet-4-20250514",
    "input_tokens": 1523,
    "output_tokens": 487,
    "module": "practice"     # diagnostic, practice, tutor, explanation
  }
}
```

The Express proxy reads `_meta` from Atlas responses and calls `logApiCall()`:

```javascript
logApiCall({
  userId: req.headers['x-atlas-student-id'],
  tool: 'atlas',
  module: responseMeta.module,
  model: responseMeta.model,
  inputTokens: responseMeta.input_tokens,
  outputTokens: responseMeta.output_tokens,
  status: 'success',
  durationMs: Date.now() - requestStart,
});
```

This flows into the same `api_calls` table and the same `AdminAnalytics.jsx` dashboard that Maven and Soar use.

---

## 9. Parallel Development Workflow

### Standalone Atlas dev (unchanged)

```bash
# Same as today
cd ~/Desktop/AI\ Tutor\ Platform
python3 -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload

# Test in browser at localhost:8000
# File-based storage, no Supabase needed
# Deploy to BASE/DEV/SB/DEPLOY with existing deploy.sh
```

### KmUnity integration dev

```bash
# Start KmUnity + Atlas together
cd ~/Desktop/KmUnity/kmunity-app
ATLAS_BACKEND_URL=http://localhost:8000 npm run dev

# Atlas Python runs on :8000 (standalone)
# KmUnity Express proxies /api/atlas/* to :8000
# KmUnity React serves on :5173 (Vite)
```

### Production (Railway)

```
Railway Project: KmUnity
├── Service 1: kmunity-app (Express + React)
│   └── Proxies /api/atlas/* to Service 2
├── Service 2: atlas-backend (Python/uvicorn)
│   └── STORAGE_BACKEND=supabase
└── Supabase (external)
```

### Feature development flow

1. Build new Atlas feature against Python backend (standalone, file-based)
2. Test with existing HTML files on localhost:8000
3. Commit to Atlas repo
4. The same Python code runs on Railway with Supabase storage
5. If the feature needs UI, update the React components (or iframe picks it up automatically)

---

## 10. Iframe-to-React Migration Path

Phase C starts with iframe embedding — Atlas's existing `index.html` loads inside KmUnity's `ToolShell`. This is fastest to ship and preserves the current student experience exactly.

Over time, individual screens can be rebuilt in React:

| Screen | Priority | Complexity | Notes |
|--------|----------|------------|-------|
| My Map / Action Plan | High | Medium | Most-viewed screen. Benefits from React state management. |
| Practice | Medium | High | Complex interaction (question → answer → feedback loop). |
| Diagnostic | Medium | Medium | Linear flow, self-contained. |
| Explore | Low | Low | Simple grid of topic cards with action badges. |
| Tutor | Low | High | Chat interface — could reuse KmUnity's `ChatInterface.jsx`. |

Each React screen replaces the iframe for that route. The Python API doesn't change — same endpoints, same responses.

---

## 11. Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Railway inter-service latency | Adds ~5-20ms per Atlas API call | Railway internal networking is fast. Profile response times; cache if needed. |
| Supabase migration data loss | Student progress lost | Run migration script with dry-run mode first. Verify row-by-row against JSON files. Keep JSON backups. |
| iframe UX inconsistency | Atlas looks different from Maven/Soar | Apply KmUnity CSS variables via postMessage theme injection. Long-term: React rebuild. |
| Dual storage divergence | File-based dev and Supabase prod drift | Storage abstraction enforces same interface. Integration tests run against both backends. |
| Safety middleware blocking Atlas responses | False positives on educational content | Tune crisis detection and content filter thresholds for educational context. Atlas system prompts already have strong guardrails. |

---

## 12. Implementation Status (as of April 5, 2026)

### Completed

- **Phase A:** Atlas Python backend deployed to Railway. Express proxy routes active. Storage abstraction (`storage.py`) with `FileStorage` and `SupabaseStorage` implementations. Supabase tables created (14 atlas_* tables). Auth bridge middleware operational. All env vars configured on Railway.
- **Phase C:** AtlasEmbed component at `/tools/atlas` with iframe embedding. Path whitelist validation (`/index.html`, `/parent.html`, `/`). Query key whitelist (`subject`, `mode`). 15-second loading timeout with error message.
- **Phase D:** Parent Hub sidebar section (parent-only visibility). ParentHubOverview page with error state handling. ParentHubAtlas page embedding parent.html. Route definitions in App.jsx.
- **Phase E:** Migration script built and run (207 rows migrated across 14 tables). `STORAGE_BACKEND=supabase` active on Railway. 007b migration converted UUID→TEXT columns for Atlas short hex IDs.

### Security Hardening (April 5, 2026 audit fixes)

- **Proxy:** Bearer token format validation, 403 on missing profile, `ATLAS_BACKEND_URL` env var guard (throws in production if missing), simplified `onProxyRes` (removed broken response buffering)
- **Backend:** All 30+ SupabaseStorage `.execute()` calls wrapped in try-except. Duplicate `api_student_stats` renamed. `list_instance_students()` and `create_instance()` wired through storage API.
- **Frontend:** AtlasEmbed path/query whitelists, loading timeout. ParentHubOverview error state. Dead code cleanup in ParentHubAtlas.

### Remaining Work

- **Phase B (partial):** Token tracking on Atlas AI calls (proxy `onProxyRes` was simplified — token interception needs reimplementation server-side). Safety middleware for Atlas AI calls. Tool activation in Supabase tools registry. Rate limiting. Session tracking.
- **Audit backlog:** Badges/feedback/book mastery still bypass storage abstraction (#1 remaining). No Supabase tables for safety logs, feedback, book mastery (#6). Performance optimizations (#15-16). Code quality items (#17-25). See `AUDIT_REPORT.md` for full list.

---

## 13. Sequencing Summary

```
Week 1:  Phase A (Foundation) — Railway deploy, proxy, storage abstraction, Supabase tables
Week 2:  Phase B (Platform) — Token tracking, safety middleware, tool registration
Week 3:  Phase C (Frontend) — AtlasLayout, iframe embed, dashboard tile, auth handoff
Week 3-4: Phase D (Parent Hub) — Sidebar restructure, overview page, Atlas progress page
Week 4:  Phase E (Cutover) — Data migration, verification, go-live
```

Standalone Atlas development continues throughout all weeks. New features land in the Python backend and are automatically available through the proxy.
