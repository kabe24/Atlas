# Atlas Code Audit Report

**Date:** April 5, 2026
**Last Updated:** April 5, 2026
**Scope:** All deployed Atlas code — backend, proxy, frontend, migrations

---

## Executive Summary

Audited the entire Atlas codebase across 20+ files. Found **10 critical issues**, **13 high severity**, and **15 medium/low** items. The most urgent problems are in the storage abstraction (several features bypass it entirely, breaking Supabase mode), the proxy auth bridge (missing validation), and the migration (unmigrated data types).

### Resolution Status (as of April 5, 2026)

| Severity | Total | Fixed | Remaining |
|----------|-------|-------|-----------|
| Critical | 7 | 5 | 2 |
| High | 8 | 6 | 2 |
| Medium | 7 | 1 | 6 |
| Low | 3 | 1 | 2 |

**Fixed items:** #1 (partial — `list_instance_students`, `create_instance`), #2, #3, #4, #5, #7 (partial), #8, #9, #10, #11, #12, #13, #14, #20, #23
**Remaining:** #1 (badges, feedback, book mastery still bypass storage), #6 (unmigrated data types), #15, #16, #17, #18, #19, #21, #22, #24, #25

---

## Critical Issues (Fix Before Production)

### 1. Several features bypass storage abstraction — broken in Supabase mode

**Files:** `app.py` — `check_and_award_badges()`, `list_instance_students()`, feedback functions, book mastery, safety logs

The storage wiring replaced the core load/save functions, but several complex functions still read files directly with `.glob("*.json")` and `json.loads(path.read_text())`. In Supabase mode (`STORAGE_BACKEND=supabase`), these directories don't exist. Badge checking, feedback, book mastery, and safety logs will silently fail or return empty data.

**Fix:** Refactor these functions to use `storage.load_lesson_log()`, `storage.load_practice_log()`, etc. Add missing methods to StorageBackend for feedback, book mastery, and safety logs.

### 2. SupabaseStorage has zero error handling ✅ FIXED

**File:** `storage.py` — entire SupabaseStorage class (lines 510-922)

Every `.execute()` call is unprotected. Network timeouts, auth failures, or schema mismatches will crash the app with unhandled exceptions rather than returning sensible defaults.

**Fix:** Wrap all `.execute()` calls in try-except. Return defaults (None, [], {}) on failure. Log errors.

### 3. Proxy auth bridge doesn't validate profile lookup ✅ FIXED

**File:** `atlas-proxy.js` lines 36-41

If the Supabase profile query returns no data (user deleted, bad token, etc.), `profile` is undefined. The code continues and sets all X-Atlas headers to undefined/empty values, allowing the request through to the Python backend with no identity.

**Fix:** Return 403 if profile lookup fails:
```javascript
if (!profile) return res.status(403).json({ error: 'Profile not found' });
```

### 4. Proxy response buffering is broken ✅ FIXED

**File:** `atlas-proxy.js` lines 84-116

The `onProxyRes` handler buffers the response body to extract `_meta` token counts. But `http-proxy-middleware` has already started streaming the response to the client. The `origWrite`/`origEnd` variables are declared but never used — dead code from an incomplete refactor. Token tracking won't work.

**Fix:** Either intercept the response stream properly (override `res.write`/`res.end` before streaming starts) or move token tracking to the Python backend, logging directly to Supabase.

### 5. Duplicate function definition shadows first version ✅ FIXED

**File:** `app.py` — two `api_student_stats` definitions

Python silently replaces the first with the second. The detailed stats implementation (counting lessons, practice, diagnostics) is unreachable.

**Fix:** Rename one or consolidate the logic.

### 6. Unmigrated data: safety logs, feedback, book mastery

**File:** `migrate_json_to_supabase.py`

The migration script handles students, profiles, diagnostics, sessions, lessons, practice, configs, and admin data. But it completely ignores: safety logs (`data/safety_logs/*.jsonl`), platform feedback (`data/platform_feedback/*.json`), and book mastery data. No Supabase tables exist for these either.

**Fix:** Create tables for these data types and add migration handlers, or document that they remain file-based only.

### 7. Race condition in instance creation ✅ PARTIALLY FIXED

**File:** `app.py` `create_instance()` (lines 703-729)

Writes parent_config and diagnostics_pending directly to disk, then updates the registry. If the registry write fails, the instance is partially created. Concurrent calls could corrupt the registry.

**Fix:** Use storage API for all writes. Add error handling for partial failures.

---

## High Severity Issues

### 8. Auth header not validated for format ✅ FIXED

**File:** `atlas-proxy.js` line 27-28

`authHeader.replace('Bearer ', '')` doesn't check if the header actually starts with "Bearer ". A "Basic" auth header would pass through with garbage as the token.

**Fix:** Check `authHeader?.startsWith('Bearer ')` before extracting.

### 9. XSS risk in iframe query parameters ✅ FIXED

**File:** `AtlasEmbed.jsx` lines 20-23

Query params from the URL are passed directly into the iframe `src`. Malicious parameters could break the URL structure.

**Fix:** Whitelist allowed query keys (`subject`, `mode`) and sanitize values.

### 10. Path traversal risk in iframe ✅ FIXED

**File:** `AtlasEmbed.jsx` line 23

The `path` prop is interpolated directly into the iframe URL. A path like `../../etc/passwd` could escape the static directory.

**Fix:** Whitelist valid paths: `/index.html`, `/parent.html`.

### 11. ParentHubOverview shows no error state ✅ FIXED

**File:** `ParentHubOverview.jsx` lines 46-49

API errors are caught and logged to console, but the UI shows "No activity this week" — misleading the parent into thinking data loaded successfully.

**Fix:** Add error state with user-visible message.

### 12. ATLAS_BACKEND_URL falls back to localhost silently ✅ FIXED

**File:** `atlas-proxy.js` line 17

If the env var is missing in production, the proxy silently targets `http://localhost:8000`, which will fail with cryptic connection errors.

**Fix:** Throw an error on startup if the env var is missing.

### 13. `list_instance_students()` still uses file I/O ✅ FIXED

**File:** `app.py` lines 875-889

This function was NOT wired through the storage abstraction. It still uses `glob("*.json")` on the filesystem. Won't work in Supabase mode.

**Fix:** Replace with `storage.list_students(instance_id)`.

### 14. Dead code: `origWrite`/`origEnd` in proxy ✅ FIXED

**File:** `atlas-proxy.js` lines 91-92

Declared but never used. Suggests the token tracking refactor was incomplete.

**Fix:** Remove or complete the implementation.

### 15. No connection pooling or caching for Supabase

**File:** `storage.py` — SupabaseStorage class

Every method call makes an independent HTTP request to Supabase. Badge checking alone triggers 15+ API calls (one per subject for profiles, lessons, practice).

**Fix:** Add simple in-memory caching for frequently accessed data like instance configs and student profiles.

---

## Medium Severity Issues

### 16. N+1 query pattern in badge checking

`check_and_award_badges()` makes separate file/API reads per subject (5+ subjects × 3 data types = 15+ calls).

### 17. Inconsistent error response formats

Some endpoints return `{"error": "..."}`, others return `{"response": ...}` or other structures.

### 18. Hardcoded "default" instead of `DEFAULT_INSTANCE_ID` constant

Multiple locations use the string `"default"` instead of the defined constant.

### 19. Missing responsive breakpoints in Atlas CSS

Only one breakpoint at 640px. iframe min-height of 600px is too tall for mobile.

### 20. AtlasEmbed has no loading timeout ✅ FIXED

If the Python backend is down, the spinner spins forever with no error message.

### 21. Header encoding — display name URL-encoded

`atlas-proxy.js` encodes the display name with `encodeURIComponent()`. Python backend must decode it, or names show as "John%20Doe".

### 22. Print statements instead of proper logging

Both `app.py` and `storage.py` use `print()` instead of Python's `logging` module.

---

## Low Severity Issues

### 23. Dead code: ParentHubAtlas imports `useAuth()` but doesn't use `profile` ✅ FIXED

### 24. Missing `aria-label` on iframe for accessibility

### 25. Console logging in production proxy code

---

## Recommended Priority

**Immediate (before using Supabase mode in production):**
1. ~~Fix #1 — Complete storage abstraction for all features~~ ✅ Partially done (core functions wired; badges/feedback/book mastery still bypass)
2. ~~Fix #2 — Add error handling to SupabaseStorage~~ ✅ Done
3. ~~Fix #3 — Validate profile in auth bridge~~ ✅ Done
4. ~~Fix #4 — Fix or remove proxy token tracking~~ ✅ Done (simplified to error logger)
5. ~~Fix #5 — Remove duplicate function definition~~ ✅ Done (renamed to `api_student_detailed_stats`)

**Next sprint:**
6. Fix #1 (remaining) — Wire badges, feedback, book mastery through storage abstraction
7. Fix #6 — Create Supabase tables and migration for safety logs, feedback, book mastery
8. Fix #15 — Add connection pooling/caching for SupabaseStorage
9. Fix #16 — Resolve N+1 query pattern in badge checking

**Backlog:**
10. Fix #17 — Inconsistent error response formats
11. Fix #18 — Hardcoded "default" instead of constant
12. Fix #19 — Mobile responsive breakpoints
13. Fix #21 — Header encoding display name
14. Fix #22 — Print statements → proper logging
15. Fix #24 — Missing aria-label on iframe
16. Fix #25 — Console logging in production proxy
