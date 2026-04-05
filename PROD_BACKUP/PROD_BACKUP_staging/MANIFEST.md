# DEPLOY Manifest — Atlas v1.3.0

**Release:** Features 57, 58, 59 — Guided Conversation, Adaptive Complexity, AI Proficiency
**Date:** 2026-03-26
**Source:** SB (tested via Chrome E2E + API-level verification)
**Test Signoff:** SB/SB_Test_Signoff_v1.3.0.docx

## What's New in v1.3.0

**Feature 59: AI Proficiency Self-Assessment** — Parents self-report their AI familiarity
(Low / Medium / High) during setup. This value is stored as `ai_proficiency` in the instance
config and drives smart defaults for Features 57 and 58. Low-proficiency families see a
3-step mini-tutorial on first student login.

**Feature 57: Guided Conversation Mode** — Two conversation modes (Guided and Open)
configurable per student from the parent dashboard. Guided mode shows follow-up suggestion
chips after AI responses and includes an "I'm Stuck" button for confusion signaling.
Single confusion triggers a re-explanation; double confusion escalates to a completely
different teaching approach. Sessions begin with a warm-up orientation message.
Smart defaults: low/medium proficiency → guided, high → open.

**Feature 58: Adaptive Response Complexity** — Calculates a complexity tier (1–4:
Foundational, Developing, Proficient, Advanced) per student per subject using a weighted
formula: diagnostic score 50%, grade level 20%, learning goals 20%, AI proficiency 10%.
Tiers are displayed on the parent dashboard with color-coded badges. Confusion signals
dynamically drop the tier by 1 for that session.

## Previous Releases in This Build

**v1.2.0 — Feature 34+: Atlas Branding + Book Mastery** (included, unchanged)

**v1.1.0 — Feature 34: Book Mastery** (included, unchanged)

## Deployable Files

```
app.py                          # Main backend (Features 57/58/59 + all prior features)
atlas_voice.py                  # AI voice/personality module (conversation mode + tier integration)
requirements.txt                # Python dependencies (unchanged)
VERSION                         # 1.3.0
.env.example                    # Environment variable template
atlas_ux_language.html          # Branding reference guide
migrations/.gitkeep             # Migration directory placeholder
tools/deploy.sh                 # Deployment helper script
static/index.html               # Student UI (F57: follow-up chips, confusion button, mini-tutorial)
static/parent.html              # Parent dashboard (F57: mode toggle, F58: tier display)
static/guide.html               # Training guide (Sections 21 + 22 added)
static/setup.html               # Instance setup wizard (F59: proficiency cards)
static/admin.html               # Admin dashboard (unchanged)
static/atlas-theme.css          # Atlas visual theme (student)
static/atlas-parent-theme.css   # Atlas visual theme (parent)
static/img/atlas-compass-rose.svg  # Brand icon
```

## Files NOT Included (by design)

- `.env` — Contains API keys; must exist on target server
- `data/` — User data; lives on PROD, never overwritten by deploys
- `*.docx` — Checklists and documentation; not runtime code
- `__pycache__/` — Python bytecode; regenerated on server start

## Bug Fixed During SB Testing

- **BUG-001:** `injectConfusionButton()` selector mismatch — looked for `#inputArea` / `.chat-input` but the actual DOM element uses class `.input-area`. Fixed in both DEV and SB before promotion.

## How to Deploy to PROD

1. Back up PROD's current `app.py`, `atlas_voice.py`, and `static/` directory
2. Copy all files from this DEPLOY folder to PROD, preserving directory structure
3. Do NOT overwrite PROD's `.env` or `data/` directory
4. Restart the PROD server: `python3 -m uvicorn app:app --host 0.0.0.0 --port 8000`
5. Verify: load the student page, test proficiency setup, test conversation mode toggle, verify complexity tiers display

## Rollback

Restore the backed-up `app.py`, `atlas_voice.py`, and `static/` directory, then restart the server.
