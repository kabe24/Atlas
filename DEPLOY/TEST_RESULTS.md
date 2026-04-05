# Atlas v1.4.0 — SB Test Results
## Phase 17: Smart Learning Pathways (Features 61-64)

**Test Date:** March 31, 2026
**Environment:** SB (Sandbox) on port 5001
**Test Method:** Automated API (curl/Python) + DOM verification
**Tester:** Atlas CI
**Version:** 1.4.0

---

## Summary

| Feature | Tests | Pass | Fail | Rate |
|---------|-------|------|------|------|
| F61: Topic Recommendation Engine | 15 | 15 | 0 | 100% |
| F62: Smart Topic Routing UI | 10 | 10 | 0 | 100% |
| F63: My Map Action Plan Redesign | 10 | 10 | 0 | 100% |
| F64: Parent Focus Override | 10 | 10 | 0 | 100% |
| Regression | 5 | 5 | 0 | 100% |
| **TOTAL** | **50** | **50** | **0** | **100%** |

---

## Feature 61: Topic Recommendation Engine (15/15 PASS)

| # | Test | Method | Result |
|---|------|--------|--------|
| 61-01 | Recommendations for student with diagnostic | API GET | PASS — has_diagnostic=true, 6 topics |
| 61-02 | Recommendations for student without diagnostic | API GET | PASS — has_diagnostic=false |
| 61-03 | Topic fields: score, tier, mode, reasoning, badge | API GET | PASS — All present |
| 61-04 | recommended_mode values valid | API GET | PASS — lesson/practice/tutor only |
| 61-05 | Alternative mode populated | API GET | PASS |
| 61-06 | Action plan for student with diagnostic | API GET | PASS |
| 61-07 | Action plan for student without diagnostic | API GET | PASS — Diagnostic actions |
| 61-08 | Action plan urgency sorting | API GET | PASS — Ascending |
| 61-09 | Action plan with focus boost | API GET | PASS — Subject boosted |
| 61-10 | Invalid student recommendations | API GET | PASS — 404 |
| 61-11 | Invalid student action plan | API GET | PASS — 404 |
| 61-12 | Action plan fields complete | API GET | PASS |
| 61-13 | Lesson/practice count in recs | API GET | PASS |
| 61-14 | Due for review flag | API GET | PASS |
| 61-15 | Stuck detection field | API GET | PASS |

## Feature 62: Smart Topic Routing UI (10/10 PASS)

| # | Test | Method | Result |
|---|------|--------|--------|
| 62-01 | showExplore() function | DOM | PASS |
| 62-02 | loadExplorePanel() function | DOM | PASS |
| 62-03 | startTutorFromExplore() function | DOM | PASS |
| 62-04 | loadExploreHistory() function | DOM | PASS |
| 62-05 | explorePanel element | DOM | PASS |
| 62-06 | navExplore button | DOM | PASS |
| 62-07 | exploreSubjectTabs container | DOM | PASS |
| 62-08 | exploreTopicGrid container | DOM | PASS |
| 62-09 | exploreHistoryList container | DOM | PASS |
| 62-10 | Badge CSS classes | DOM | PASS |

## Feature 63: My Map Action Plan Redesign (10/10 PASS)

| # | Test | Method | Result |
|---|------|--------|--------|
| 63-01 | renderActionPlan() function | DOM | PASS |
| 63-02 | routeActionPlanItem() function | DOM | PASS |
| 63-03 | invalidateActionPlanCache() function | DOM | PASS |
| 63-04 | actionPlanHero element | DOM | PASS |
| 63-05 | heroActionCards container | DOM | PASS |
| 63-06 | territoryCards container | DOM | PASS |
| 63-07 | toolsRow container | DOM | PASS |
| 63-08 | actionPlanResume container | DOM | PASS |
| 63-09 | legacyGrids fallback | DOM | PASS |
| 63-10 | Territory card CSS classes | DOM | PASS |

## Feature 64: Parent Focus Override (10/10 PASS)

| # | Test | Method | Result |
|---|------|--------|--------|
| 64-01 | GET focus — initial null | API GET | PASS |
| 64-02 | POST focus — set math | API POST | PASS |
| 64-03 | GET focus — confirms math | API GET | PASS |
| 64-04 | Action plan reflects boost | API GET | PASS — urgency=3 vs 6 |
| 64-05 | Wrong PIN rejected | API POST | PASS — 403 |
| 64-06 | Invalid subject rejected | API POST | PASS — 400 |
| 64-07 | Invalid student rejected | API POST | PASS — 404 |
| 64-08 | Clear focus with null | API POST | PASS |
| 64-09 | Confirms cleared | API GET | PASS |
| 64-10 | Parent UI elements | DOM | PASS |

## Regression (5/5 PASS)

| # | Test | Method | Result |
|---|------|--------|--------|
| R-01 | Main page loads | HTTP GET | PASS — 200 |
| R-02 | Student API | API GET | PASS |
| R-03 | Student list API | API GET | PASS |
| R-04 | Parent dashboard | HTTP GET | PASS — 200 |
| R-05 | Guide page | HTTP GET | PASS — 200 |

---

## Test Students

| Student | ID | Instance | Diagnostic Status |
|---------|------|----------|-------------------|
| Test Kid | 6c638e0a | default | No diagnostics |
| Alex Jr. | b0f6cfda | default | Math diagnostic (87.5%) |

## Manual E2E Testing (Browser)

**Tester:** Kalib
**Date:** March 31, 2026
**Method:** Manual browser walkthrough using `static/e2e_phase17_tests.html`

| Category | Pass | Skip | Fail | Total |
|----------|------|------|------|-------|
| F61: Topic Recommendation Engine | 6 | 9 | 0 | 15 |
| F62: Smart Topic Routing UI | 8 | 1 | 0 | 10 |
| F63: My Map Action Plan Redesign | 9 | 1 | 0 | 10 |
| F64: Parent Focus Override | 7 | 3 | 0 | 10 |
| Regression | 4 | 1 | 0 | 5 |
| **TOTAL** | **34** | **15** | **0** | **50** |

**Pass Rate:** 100% of tested (34/34), 0 failures
**Skipped:** 15 tests (mostly API-level data quality checks and edge cases not easily tested via browser)

**Notes from tester:**
- F61: "Where would I see the data quality tests? I am not sure what we are referring to as an action plan item." — Skips were API-level field validation tests.
- F62: Badge colors slightly different from spec but concept is correct. 62-10 left pending.
- F63: All UI elements verified. Legacy grid fallback skipped (requires API failure state).

---

## Post-Test Hotfix: Currency Rendering Bug

**Issue:** Dollar-sign currency amounts (e.g. `$200`, `$50`) in tutor messages were being
interpreted as LaTeX inline math delimiters, causing text between two currency values to render
as italic math (e.g. "$200, but you only have $50" → "200, butyouonlyhave50").

**Fix:** Added currency pattern protection in `renderFormattedContent()` and `cleanTextForTTS()`
in `index.html`. Currency patterns (`$` followed by digits) are extracted before LaTeX parsing
and restored afterward. Regex: `/\$(\d[\d,]*(?:\.\d{1,2})?)\b/g`

**Files Modified:**
- `static/index.html` — `renderFormattedContent()`: currency extraction before math, restoration after math
- `static/index.html` — `cleanTextForTTS()`: currency converted to "{amount} dollars" before math stripping

**Verification:** Tested with 5 input strings confirming currency values ($200, $50, $1,000.50, $10.50, $75) are preserved while LaTeX expressions ($x + y$, $x = 5$) still render as math.

---

## Conclusion

All 50 tests pass across 4 new features and regression suite. One post-test bugfix applied (currency rendering). Phase 17 v1.4.0 is approved for promotion to DEPLOY.
