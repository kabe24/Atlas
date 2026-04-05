# DEPLOY Manifest — Atlas v1.4.0

**Release:** Phase 17 — Smart Learning Pathways (Features 61-64)
**Date:** 2026-03-31
**Source:** SB (tested via automated API + DOM verification, 50/50 pass)
**Previous Version:** v1.3.3

---

## What's New

### Feature 61: Topic Recommendation Engine
Backend intelligence that analyzes a student's full learning history and returns per-topic recommendations: Learn (Expedition), Practice, or Talk to Tutor. Includes stuck detection, spaced review awareness, and a cross-subject action plan.

### Feature 62: Smart Topic Routing UI
New "Explore" panel accessible from the sidebar. Shows every topic with an action badge (Learn/Practice/Tutor/Strong), inline routing prompts, and combined lesson+practice history. Clicking a routing button goes directly to the recommended activity.

### Feature 63: My Map Action Plan Redesign
Welcome screen redesigned from navigation menu to personalized action plan. Shows "What to Do Next" hero section (top 3 priorities), territory cards (per-subject status with recommended actions), resume banners for active sessions, and always-available tools row.

### Feature 64: Parent Focus Override
Parents can set a "Focus This Week" subject per student from the dashboard Settings tab. Boosted subject's actions appear at the top of the student's My Map. Requires parent PIN. Persists until cleared.

---

## New API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/subject/recommendations/{subject}` | GET | Per-topic recommendations for a subject |
| `/api/recommendations/action-plan/{student_id}` | GET | Top priority actions across all subjects |
| `/api/instance/{instance_id}/student/{student_id}/focus` | GET | Get current focus subject |
| `/api/instance/{instance_id}/student/{student_id}/focus` | POST | Set/clear focus subject (PIN auth) |

## Post-Test Hotfix

**Currency rendering bug:** Dollar-sign currency in tutor messages (e.g. `$200`, `$50`) was interpreted as LaTeX math delimiters. Fixed by adding currency pattern protection in `renderFormattedContent()` and `cleanTextForTTS()`.

## Files Modified

| File | Changes |
|------|---------|
| `app.py` | +4 API endpoints, recommendation engine, focus override (~250 lines) |
| `static/index.html` | Explore panel, action plan redesign, nav wiring (~500 lines), currency rendering fix |
| `static/parent.html` | Focus Subject UI in Settings tab (~80 lines) |
| `VERSION` | 1.3.3 → 1.4.0 |

## New Infrastructure (Added Post-v1.4.0)

### Storage Abstraction Layer
| File | Description |
|------|-------------|
| `storage.py` | `StorageBackend` base class with `FileStorage` and `SupabaseStorage` implementations. All data I/O in `app.py` delegates to `storage.*()` methods. Controlled by `STORAGE_BACKEND` env var. |

### Supabase Migrations
| File | Description |
|------|-------------|
| `migrations/007_atlas_tables.sql` | Creates 14 atlas_* tables with RLS policies |
| `migrations/007b_atlas_tables_text_ids.sql` | Converts UUID columns to TEXT for Atlas short hex IDs |
| `migrations/migrate_json_to_supabase.py` | JSON→Supabase migration script (dry-run support, idempotent) |
| `migrations/CUTOVER_CHECKLIST.md` | Step-by-step production cutover procedure |

### Audit & Hardening
| File | Description |
|------|-------------|
| `AUDIT_REPORT.md` | Full code audit findings and resolution status |

## Dependencies

**Python packages** (see `requirements.txt`):
- `supabase` — required for Supabase storage backend

No new npm packages. Configuration changes: `STORAGE_BACKEND`, `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` env vars (see `.env.example`).

## Deploy Instructions

1. Backup current PROD to PROD_BACKUP
2. Copy DEPLOY files to PROD (exclude `data/` directory)
3. Restart PROD server
4. Verify: `curl http://localhost:PORT/api/recommendations/action-plan/STUDENT_ID?instance_id=default`
5. Verify: Main page loads with action plan hero section

## Rollback

If issues found, restore from PROD_BACKUP. Student data is not affected (stored in `data/` directory which is excluded from deploys).

## Test Coverage

- 50 automated tests (15 F61 + 10 F62 + 10 F63 + 10 F64 + 5 regression): 50/50 PASS (100%)
- 50 manual E2E browser tests via `static/e2e_phase17_tests.html`: 34 pass, 15 skip, 0 fail
- See `SB/TEST_RESULTS.md` and `SB/SB_Test_Signoff_v1.4.0.docx` for details
