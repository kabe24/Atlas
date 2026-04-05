# Atlas Development Plan
## Adaptive 6th–12th Grade Tutor — Feature Roadmap

**Student:** 6th–12th Grader
**Subjects:** Math, Science, English/Language Arts, Social Studies, Latin
**Platform:** Web Application (no-code — AI-generated)
**AI Engine:** Claude API (Anthropic)
**Data Storage:** Local (SQLite + JSON files)
**Build Method:** Claude generates all code — you run commands
**Approach:** Iterative — ship early, layer features
**Last Updated:** March 24, 2026
**Grade Range:** 6–12 (with grade-aware content planned in Feature 25)

### Current Build Status

| Phase | What's Included | Status |
|-------|-----------------|--------|
| Phase 1 | Backend, SQLite, subject/topic data model, chat API, diagnostic engine | Complete |
| Phase 2 | 5-step structured lessons, adaptive topic selection, step tracking, resume | Complete |
| Phase 3 | Single-page UI, sidebar nav, mode switching, lesson picker, progress bars | Complete |
| Phase 4 | API endpoint tests (61/61), Chrome browser tests (80/80) | Complete |
| Phase 5 | Practice engine with exercises, hints, streaks, and difficulty scaling | Complete |
| Phase 6 | Student accounts with PIN auth, multi-student support, badges, data isolation | Complete |
| Phase 7 | Parent progress dashboard with charts, stats, and activity history | Complete |
| Phase 8 | Multi-tenancy with instance management, data migration, instance-scoped auth | Complete |
| Phase 9 | Platform customization, custom subjects, branding, feature flags | Complete |
| Phase 10 | Ad hoc diagnostics, parent-initiated assessments, delete controls | Complete |
| Phase 11 | Feedback mechanism, approval workflow, admin dashboard | Complete |
| Phase 12 | Parent PIN management, path-based instance URL routing, add student | Complete |
| Phase 12.5 | Beta testing & remote access via Cloudflare Tunnel, full instance-aware student APIs | Complete |
| Feature 20 | Math rendering with KaTeX for STEM subjects | Complete |
| E2E Testing | 65-test interactive checklist covering all features, clean instance verification | Complete |
| Feature 23 | Product tour, help section, and training guide | Complete |
| Phase 13 | Gamification & invite links | Complete |
| Feature 24 | Onboarding intake form — self-service family setup | Complete |
| Feature 18 | Socratic mode — parent-controlled guided questioning | Complete |
| Feature 21 | Quick quiz & flashcard study mode | Complete |
| Feature 16 | Schoolwork upload — AI analysis, practice generation, grade tracking, curriculum integration | ✅ Complete |
| Phase 15 | AI Accessibility & User Proficiency — guided conversation, adaptive complexity, onboarding, activity templates | In Progress (Feature 60 remaining) |
| Phase 17 | Smart Learning Pathways — recommendation engine, unified topic routing, My Map action plan redesign, parent focus override | ✅ Complete (Features 61-64) |
| Phase 16 | Study timer (Pomodoro), voice I/O (speech-to-text & TTS) | ✅ Complete |
| Feature 25 | Grade scaling (6–12) — dynamic grade-aware prompts, topics, and safety rules | ✅ Complete |
| Feature 26 | ADD/ADHD adaptability — chunking, pacing, refocus, session presets, reduced load | Planned |
| Feature 27 | Parent safety transparency — visible content rules, safety log UI, conversation review | ✅ Complete |
| Feature 28 | Standards alignment — Common Core (Math & ELA), NGSS (Science), state standards (Social Studies), per-domain mastery, parent & student reports | ✅ Complete |
| Feature 29 | Admin dashboard — instance management, feedback responses, student oversight, safety moderation, invite management, usage analytics, system health | ✅ Complete (29A-G) |
| Feature 30 | Family referral program — unique codes, two-sided rewards, tiered incentives, Stripe billing credits | Planned |
| Feature 34 | Book Mastery — chapter-by-chapter comprehension verification, bookshelf, XP rewards | ✅ Complete |
| Phase 14 | Atlas Brand Adoption — visual theme, AI voice system, UX language, compass rose logo, background watermarks | ✅ Complete |

---

## Phase 14: Atlas Brand Adoption

**Status: Complete | Priority: High**

Atlas is the student-facing brand identity for the KmUnity Learning Tool. This phase adopts the full Atlas brand across the student experience: visual theme, AI voice, UX language, and background imagery.

### Feature 51: Visual Theme (`atlas-theme.css`)
**Status: Complete**

Complete CSS design token system overriding existing variables. Loaded via `<link rel="stylesheet" href="/static/atlas-theme.css">` after the inline styles in `index.html`.

- **Color Palette:** Midnight (#0B1D3A), Deep Ocean (#14305A), Explorer Blue (#1E4D8C), Compass Gold (#D4A843), Warm Amber (#E8B84B), Lantern Glow (#F4CE6A), Parchment (#F5EFE0), Teal Pin (#2A9D8F), Coral Pin (#E76F51), Forest Green (#4A7C59), Mountain Slate (#6B7B8D)
- **Typography:** Outfit (display), Crimson Pro (editorial), DM Mono (data) via Google Fonts
- **Components styled:** Sidebar, chat bubbles, buttons, cards, progress bars, inputs, scrollbars, mode selectors, status indicators

### Feature 52: AI Voice System (`atlas_voice.py`)
**Status: Complete**

Two-tier voice system with grade-based selection:
- **Middle School (grades 6–8):** Warmer, more metaphorical, exploration-heavy language
- **High School (grades 9–12):** Mature conversational peer tone
- `wrap_atlas_voice(base_system_prompt, grade)` prepends Atlas identity + voice + UX language note
- Wired into `build_lesson_system_prompt()`, `build_practice_system_prompt()`, and main chat handler in `app.py`

### Feature 53: UX Language
**Status: Complete**

Hybrid approach: student-facing surfaces use Atlas exploration vocabulary; parent/teacher dashboards keep traditional academic metrics.

| Old Term | Atlas Term | Where Used |
|----------|-----------|------------|
| Home | My Map | Sidebar nav |
| Lessons | Expeditions | Sidebar, section headers |
| Practice | Practice (unchanged) | Sidebar |
| Subjects | Territories | Sidebar section header |
| Badges | Landmarks | Gamification shelf |
| Streak | Expedition Streak | Stats display |
| Tutor | Atlas Guide | Chat header |

### Feature 56: Background Watermarks
**Status: Complete**

Subtle SVG watermark imagery gives Atlas screens visual texture:

- **Login screen:** Full-viewport wireframe globe (latitude/longitude lines) in Compass Gold at 15% opacity, baked into `index.html` inline CSS. Size: `150vmin` to fill the background.
- **Main content area:** Compass rose with N/S/E/W labels anchored bottom-right at 7% opacity, plus faint lat/long grid lines at 2.5% opacity. Applied via `.main` background in `atlas-theme.css`.
- **Sidebar:** Topographic contour lines in Compass Gold at 12% opacity, positioned at the bottom 50% of the sidebar via `::after` pseudo-element.

All watermarks use inline SVG data URIs (no extra file requests) and `pointer-events: none` so they don't interfere with interaction.

### Bug Fix: atlas-theme.css Path
The original `<link>` tag used a relative path (`href="atlas-theme.css"`) which resolved to `/atlas-theme.css` (404). Fixed to `href="/static/atlas-theme.css"` to match the FastAPI static mount at `/static/`.

### Bug Fix: Panel-Switching Consistency (March 24, 2026)
Multiple panel-switching functions in `index.html` were missing hide calls for sibling panels, causing "sticky" overlays when navigating between views. The original bug: clicking a subject (e.g. Science) while on the Standards view left `#standardsPanel` visible behind `#chatContainer`.

**Root cause:** Each function only hid the panels it "knew about" when originally written — newer panels (Standards, Profile) weren't added to older functions.

**Functions patched (8 total):**
- `selectSubject()` — added `#standardsPanel`, `#profilePanel`, `navStandards`, `navLessons`, `profileBtn` cleanup
- `showResults()` — added `#profilePanel`
- `showLessonPicker()` — added `#profilePanel`
- `showPracticePicker()` — added `#profilePanel`
- `showProfileHub()` — added `#standardsPanel`
- `startLesson()` / `resumeLesson()` — added `#practicePanel`, `#studyPanel`, `#standardsPanel`, `#profilePanel`
- `startPractice()` / `resumePractice()` — added `#studyPanel`, `#standardsPanel`, `#profilePanel`

All panel transitions now follow a consistent pattern: every function hides all 8 panels, then shows only its target.

### Feature 54: Parent Portal Visual Refresh
**Status: Complete**

Created `atlas-parent-theme.css` — a standalone CSS override file for `parent.html` that maps the existing CSS variables to Atlas design tokens.

- **Typography:** Outfit (display), Crimson Pro (editorial), DM Mono (data) via Google Fonts `@import`
- **Color Palette:** All `:root` variables remapped to Atlas tokens (Midnight, Deep Ocean, Explorer Blue, Compass Gold, Parchment, Teal Pin, Coral Pin, etc.)
- **Login Screen:** Gradient updated to Midnight → Deep Ocean
- **Dashboard Components:** Metric cards use Warm Cream backgrounds, Soft Linen borders, Deep Ocean value text
- **Proficiency Tiers:** Advanced (Explorer Blue), Proficient (Teal Pin), Developing (Warm Amber), Needs Work (Coral Pin)
- **Scrollbar:** Styled to match student theme
- **Watermark:** Compass rose SVG on `.dash-main` at 5% opacity, bottom-right
- **Page title:** Updated from "Parent Dashboard — Atlas" to "Parent Dashboard — Atlas"
- **Loaded via:** `<link rel="stylesheet" href="/static/atlas-parent-theme.css">` after inline styles in parent.html

### Feature 55: Help Content & Glossary Update
**Status: Complete**

Updated all help surfaces with Atlas terminology and visual branding:

**guide.html (Training Guide):**
- Title: "Training Guide — Atlas"
- Header: "🧭 Atlas Training Guide" with Midnight→Deep Ocean gradient
- CSS variables remapped to Atlas palette (Parchment background, Midnight text, etc.)
- Fonts: Outfit via @import
- Callout colors updated to Atlas-tinted greens, blues, and ambers
- Terminology updated throughout: "Atlas" → "Atlas", "subjects" → "territories", "lessons" → "expeditions", "badges" → "landmarks", "Home" → "My Map", "the tutor" → "Atlas" / "your Atlas guide"

**parent.html (Parent Help & FAQ):**
- Dashboard Overview icon changed from 🏠 to 🧭
- All "Atlas" → "Atlas", "subjects" → "territories", "lessons" → "expeditions"
- "tutor" → "Atlas" in Socratic Mode, Safety, Grade Scaling, Adaptive Learning, and Standards sections
- FAQ answers updated: custom subjects → custom territories, lessons → expeditions
- Invite section: "Atlas" → "Atlas instance"

**index.html (Student Help & FAQ):**
- Getting Started: "home screen" → "My Map", "subjects" → "territories", "tutor" → "Atlas"
- Diagnostics: "Click any subject" → "Click any territory"
- Lessons → Expeditions, Badges → Landmarks
- Study Plan: "home screen" → "My Map"
- Grade Scaling: "The tutor" → "Atlas", "Lessons" → "Expeditions"
- Safety: "The tutor" → "Atlas"

---

## Architecture Overview

### No-Code Build Approach

You will not write or edit any code. Claude generates all application code, configuration files, and database schemas. Your role is limited to:

- **Running terminal commands** — Copy-paste commands that Claude provides into Terminal
- **One-time setup** — Installing Python and getting an Anthropic API key
- **Testing features** — Use the tutor in your browser and give feedback
- **Uploading schoolwork** — Through the web interface

Each feature is delivered as a complete, working code package. If something needs to change, you describe what you want and Claude regenerates the code.

### Tech Stack

All technology choices are optimized for simplicity. You don't need to understand any of this — it's listed here for reference.

- **Frontend** — HTML/CSS/JS — auto-generated, no frameworks to learn
- **Backend** — Python + FastAPI — Claude writes all server code
- **AI** — Claude API via the Anthropic Python SDK — handles all AI interactions
- **Database** — SQLite — a single local file, no database server to manage
- **Deployment** — Runs locally on your Mac — open localhost in any browser

---

## Session Planning Guide

Before each development session, take 2–3 minutes to write down your priorities. This keeps sessions focused, avoids losing time figuring out where to start, and becomes especially important as features grow in complexity (adaptive engine, schoolwork upload, etc. will span multiple sessions).

**Before starting, answer these three questions:**

1. **What feature or task are we working on?** — Name the specific feature number and any sub-component (e.g., "Feature 23 — product tour, specifically the first-time walkthrough overlay").
2. **What does "done" look like for this session?** — Be specific: "Backend endpoints tested and working" is better than "make progress on the feature."
3. **Are there any decisions or blockers to resolve first?** — Note anything you've been thinking about since the last session (design preferences, changed requirements, bugs you noticed).

Paste your answers into the chat at the start of each session. This gives Claude immediate context and saves the back-and-forth of figuring out what to build next.

---

## Feature 1: Core Tutor Conversation Engine
**Must-Have | Week 1–2 | Status: Complete**

### What It Does
The foundational chat interface where your son interacts with the AI tutor. He selects a subject, and Claude responds in the role of a knowledgeable, patient tutor calibrated for 8th grade.

### Key Components

- **Subject selector** — Choose from Math, Science, ELA, Social Studies, or Latin before starting a session
- **Chat interface** — Clean, simple text conversation with the tutor
- **System prompt engineering** — Claude is instructed to act as an 8th grade tutor: explain concepts clearly, use age-appropriate language, encourage effort, and stay mostly academic
- **Session management** — Each conversation is a "session" tied to a subject and date
- **Conversation history** — Previous messages in the session are passed to Claude for context continuity

### Acceptance Criteria

- [x] Student can select a subject and start a conversation
- [x] Claude responds as a tutor appropriate for an 8th grader
- [ ] Off-topic requests get a gentle redirect back to academics
- [x] Conversation persists within a session
- [x] Sessions are saved locally with timestamps

---

## Feature 2: Diagnostic Assessment System
**Must-Have | Week 2–3 | Status: Complete**

### What It Does
An initial placement assessment for each subject that identifies your son's current knowledge level, strengths, and gaps. This becomes the foundation for personalized lesson planning.

### Key Components

- **Subject-specific question banks** — 15–25 questions per subject spanning key 8th grade topics, from foundational to advanced
- **Adaptive questioning** — Claude generates follow-up questions based on responses to dig deeper into weak areas
- **Skill mapping** — Each question maps to a specific skill or topic area
- **Scoring and gap identification** — After the diagnostic, produce a skill profile showing mastery levels per topic

### Subject Breakdown (8th Grade)

| Subject | Key Topic Areas |
|---------|----------------|
| **Math** | Rational/irrational numbers, linear equations, functions, geometry, statistics & probability, exponents |
| **Science** | Forces & motion, energy, waves, Earth's systems, genetics & heredity, ecosystems, scientific method |
| **ELA** | Reading comprehension, textual analysis, argumentative writing, grammar & mechanics, vocabulary in context |
| **Social Studies** | US History (Constitution through Reconstruction), civics & government, geography, economics basics |
| **Latin** | Vocabulary (common roots/prefixes), noun declensions, verb conjugations, basic translation, Roman culture |

### Scoring Model

| Level | Score Range | Meaning |
|-------|------------|---------|
| Needs Work | 0–40% | Significant gaps — start lessons here |
| Developing | 41–70% | Partial understanding — reinforce and practice |
| Proficient | 71–90% | Solid grasp — maintain and extend |
| Advanced | 91–100% | Strong mastery — challenge with enrichment |

### Acceptance Criteria

- [x] Diagnostic available for all 5 subjects
- [x] Questions adapt based on student responses
- [x] Results produce a per-topic skill profile
- [x] Skill profiles are saved locally and used by the lesson engine
- [x] Student gets a friendly summary of results

### Feature 2 Test Results — PASSED (March 4, 2026)

Full end-to-end testing completed via automated browser testing. All acceptance criteria verified.

Math Diagnostic (16 questions): Covered all 6 topic areas. Questions adapted based on responses — intentionally wrong answer on Functions triggered easier follow-up and correctly lowered that topic's score to 70% while others scored 85–95%.

Diagnostic Results Panel: Per-topic scores displayed with color-coded mastery levels. Other subjects correctly show "No diagnostic taken yet" with links to start.

Completion Behavior: Progress bar fills completely, input disables with "Assessment complete!" message, "View Results" button appears. Welcome screen shows green "Completed" badge.

---

## Feature 3: Personalized Lesson Generator
**Must-Have | Week 3–4 | Status: Complete**

### What It Does
Using diagnostic results, the tutor generates tailored lessons that target gaps while reinforcing strengths. Lessons adapt in real-time based on how the student is responding.

### Key Components

- **Lesson planning engine** — Claude receives the student's skill profile and generates a lesson plan prioritizing weak areas
- **Lesson delivery** — Each lesson includes concept explanation, worked examples, guided practice, and independent practice
- **Adaptive pacing** — If the student grasps a concept quickly, move on. If struggling, slow down and try a different approach
- **Mixed/adaptive approach** — Sometimes teach first then practice, sometimes problem-first — Claude chooses based on the student's responses

### Lesson Structure (5-Step Flow)

- **1. HOOK (2 min)** — Connect to something interesting or previously learned
- **2. CONCEPT (5–10 min)** — Clear explanation with 1–2 examples. Check for understanding.
- **3. GUIDED PRACTICE (5–10 min)** — 2–3 problems worked together. Hints available if stuck.
- **4. INDEPENDENT PRACTICE (10–15 min)** — 3–5 problems on his own. Immediate feedback after each.
- **5. WRAP-UP (2 min)** — Summary of what was learned. Preview of next lesson.

### Acceptance Criteria

- [x] Lessons are generated based on the diagnostic skill profile
- [x] Lesson difficulty matches the student's current level per topic
- [x] Claude adapts its teaching approach mid-lesson based on responses
- [x] Lessons are logged with topic, date, and completion status
- [x] Student can resume an incomplete lesson

---

## Feature 4: Exercise & Practice Engine
**Must-Have | Week 4–5 | Status: Complete**

### What It Does
A dedicated practice mode where the student can drill specific skills with generated exercises. Includes immediate feedback, hints, and step-by-step solutions.

### Key Components

- **On-demand practice** — Student can request practice on any topic at any time
- **Difficulty scaling** — Problems start at the student's current level and adjust up/down based on streaks
- **Hint system** — 3-tier hints: (1) gentle nudge, (2) strategy hint, (3) first step shown
- **Immediate feedback** — After each answer, explain what was right or where the mistake was
- **Streak tracking** — Track consecutive correct answers with animated fire counter to build momentum

### Exercise Types by Subject

| Subject | Exercise Formats |
|---------|-----------------|
| **Math** | Solve equations, word problems, graph interpretation, proofs, multiple choice |
| **Science** | Concept questions, diagram labeling (text-based), experiment design, data interpretation |
| **ELA** | Reading passages + questions, grammar correction, vocabulary in context, short writing prompts |
| **Social Studies** | Primary source analysis, timeline ordering, cause-and-effect, map/data interpretation |
| **Latin** | Vocabulary matching, declension/conjugation drills, translation, root word identification |

### Implementation Details

- **6 API endpoints** — start, answer, hint, active, log, end — all tested via curl
- **Practice picker UI** — Topic grid with diagnostic score badges, recommended topic, resume banner, session history
- **Stats bar** — Real-time display of streak count, questions answered, correct count, accuracy %, and difficulty badge
- **Difficulty auto-scaling** — 3 correct in a row bumps difficulty up; 2 wrong in a row drops it down. Initial difficulty from diagnostic score (<50% = easy, 50–80% = medium, >80% = hard)
- **Structured markers** — ===QUESTION===, ===FEEDBACK===, ===HINT_1/2/3===, ===PRACTICE_COMPLETE=== for reliable parsing
- **JSON file persistence** — Practice sessions and history logs stored in data/practice/ directory

### Acceptance Criteria

- [x] Practice mode available for all subjects and topic areas
- [x] Difficulty adjusts based on performance within the session
- [x] Hint system works with 3 escalating levels
- [x] Each exercise result is logged (topic, difficulty, correct/incorrect, time spent)
- [x] Student can see their streak count during practice

### Feature 4 Test Results — PASSED (March 4, 2026)

Full implementation testing completed. All 6 practice API endpoints tested via curl with correct responses. Chrome browser tests verified: practice picker renders with topic grid, score badges, and recommended topics; practice session UI shows stats bar with streak counter, difficulty badge, hint button, and question/accuracy tracking.

Practice Picker: All 6 Math topics displayed with color-coded diagnostic scores. Weakest topic recommended. Resume banner shows for active sessions. Practice history section lists completed sessions.

Practice Session UI: Stats bar renders with fire streak counter (0), question/correct/accuracy counters, MEDIUM difficulty badge, and Hint button with 3 remaining. Difficulty badge is color-coded (green=easy, yellow=medium, red=hard).

Note: Full interactive flow (starting session, answering questions, using hints, completing session) requires the Claude API which cannot be reached from the test sandbox. Manual testing on a local machine is recommended.

---

## Feature 5: Student Accounts & Personalization
**P2 (High) | Sprint 3 | Status: Complete**

### What It Does
Multi-student support with PIN-based authentication and complete data isolation. Each student gets their own login screen with card selection, personalized profile hub with achievement badges, and isolated data directories. The tutor addresses each student by name and remembers their progress across all modes.

### Key Components

- **Multi-student support** — Each student has an isolated account with 4-digit PIN authentication
- **Login screen** — Student card selection with numeric PIN pad entry
- **Account creation** — Quick form with name, PIN, avatar picker (20 emojis), and grade selector (6–12)
- **Profile hub** — Shows student name, avatar, grade, and statistics (diagnostics completed, lessons completed, practice sessions, accuracy)
- **Badge system** — 10 achievement badges awarded automatically: First Steps, Full Picture, Eager Learner, Lesson Veteran, Practice Makes Perfect, Practice Pro, High Achiever, Perfect Score, Dedicated Learner, Well Rounded
- **Data namespacing** — Each student gets isolated directories: sessions, diagnostics, lessons, practice
- **System prompt personalization** — Claude addresses students by name in all responses
- **Legacy data migration** — Utility to move flat data into student-namespaced directories
- **Logout functionality** — Returns to login screen

### Backend Components

- **Student models** — StudentCreateRequest, StudentLoginRequest, StudentUpdateRequest, StudentMigrateRequest
- **Student helpers** — load_student, save_student, list_students
- **8 API endpoints** — /api/students, /api/student/{id}, /api/student/create, /api/student/login, /api/student/update, /api/student/stats/{id}, /api/student/{id}/badges, /api/student/migrate
- **Badge engine** — BADGES dict with definitions, check_and_award_badges() function
- **student_id threading** — Threaded through ALL existing route handlers (chat, diagnostic, lesson, practice)
- **Data path helpers** — Updated for student namespacing (session_path, profile_path, diagnostic_path, lesson_path, practice_path, etc.)

### Frontend Components

- **Login screen** — Existing Student tab with card selection and PIN entry pad
- **Create Account tab** — Account creation form with avatar grid and grade picker
- **PIN entry pad** — 4-digit PIN with visual indicator dots
- **Profile hub** — Stats cards showing diagnostics completed, lessons completed, practice sessions, accuracy
- **Badge shelf** — Badge display and toast notifications on new achievements
- **Helper functions** — apiUrl() and apiBody() for threading both student_id and instance_id throughout all API calls
- **Sidebar personalization** — My Profile and Logout buttons, student name/avatar/grade display
- **Inactivity auto-logout** — 30-minute idle timer resets on click/keydown/mousemove/touch/scroll; shows alert and returns to login

### Robustness & Data Safety

- **safe_json_load() helper** — Centralized JSON loader with error handling for corrupted, empty, or missing files. Backs up corrupt files as .corrupt before returning defaults.
- **All data loaders use safe_json_load** — load_student, load_session, load_diagnostic, load_profile, load_lesson, load_lesson_log, load_practice, load_practice_log all protected
- **Atomic writes** — All save functions use tmp-file-then-rename pattern to prevent partial writes on crash
- **Server restart required** — uvicorn should be started with `--reload` flag during development so file changes auto-restart the server (e.g., `python3 -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload`). Without this flag, the server must be manually restarted after code changes.

### Testing Checklist

- [x] Create student account
- [x] List students
- [x] Login with correct PIN
- [x] Login with wrong PIN rejected
- [x] Get student profile
- [x] Update student details
- [x] Get student stats
- [x] Get student badges
- [x] Migrate legacy data
- [x] Data isolation between students
- [x] Browser login flow
- [x] Browser create account flow
- [x] Browser profile hub
- [x] Browser logout
- [x] Inactivity auto-logout (30-min timer)
- [x] safe_json_load handles corrupted files
- [x] safe_json_load handles missing files
- [x] Data migration copies sessions, profiles, diagnostics, lessons, practice
- [x] Data migration triggers badge check
- [x] Auto-reload server starts with --reload flag

---

## Feature 5.5: Content Safety Guardrails
**Must-Have | Week 5 | Status: Complete**

### What It Does
A multi-layered content safety system ensuring all AI-generated content is age-appropriate for an 8th grader (ages 12–14). Protects against inappropriate content, prompt injection attacks, and off-topic conversations.

### Safety Layers
- **System prompt hardening** — All 4 system prompts (chat, diagnostic, lesson, practice) include CONTENT_SAFETY_RULES requiring age-appropriate clinical/scientific language, subject-locking, and refusal to reveal instructions
- **Input filtering** — `check_message_safety()` screens every student message before it reaches Claude, checking against regex patterns for blocked topics and injection attempts
- **Blocked topic detection** — Regex patterns catch requests for explicitly harmful content (violence, drugs, self-harm, explicit material) and return a safe redirect message
- **Prompt injection protection** — 15 regex patterns detect attempts to override instructions, role-play, reveal system prompts, or activate jailbreak modes
- **Subject locking** — System prompts instruct Claude to redirect off-topic questions back to the current subject
- **Conversation logging** — Every chat turn is logged per-student in `conversation_log.jsonl` for parent review via `/api/student/{id}/conversation-log`
- **Safety event logging** — Blocked messages and injection attempts are logged to `data/safety_logs/` with timestamps, patterns matched, and message previews
- **Parent review API** — `/api/safety-log` returns recent safety events; `/api/student/{id}/conversation-log` returns a student's conversation history

### Content Safety Rules (appended to all system prompts)
- **Age-appropriate language** — Clinical/scientific terminology only for sensitive topics; no graphic descriptions, slang, or innuendo
- **Subject boundary enforcement** — Polite redirect when student asks about topics outside current subject
- **Role-play refusal** — Declines attempts to change persona or discuss non-academic topics
- **Instruction concealment** — Never reveals system prompt, instructions, or internal rules
- **Inappropriate language redirect** — Gently redirects without repeating the language
- **Conservative default** — Errs on the side of caution when content appropriateness is uncertain

### Acceptance Criteria
- [x] System prompt safety rules appended to all 4 prompt types
- [x] Blocked topic regex catches harmful content requests
- [x] Prompt injection regex catches 15 attack patterns
- [x] check_message_safety returns safe redirect for blocked messages
- [x] Safety events logged to daily JSONL files
- [x] Conversation turns logged per-student for parent review
- [x] /api/student/{id}/conversation-log endpoint returns log entries
- [x] /api/safety-log endpoint returns recent safety events
- [x] Normal academic messages pass safety check
- [x] App imports and starts cleanly with all safety code

---

## Feature 6: Parent Progress Dashboard
**Must-Have | Week 6–7 | Status: Complete**

### What It Does
A visual web dashboard (separate from the student view) where a parent can monitor their child's progress, see where they're improving, and identify areas that need attention. Accessible at /parent with PIN-based authentication.

### Key Components

- **PIN-based parent login** — Separate 4-digit PIN (default 0000), changeable via /api/parent/setup. Keyboard support for PIN entry.
- **Student selector** — Dropdown in header lists all students; switching students reloads all dashboard data via a single API call.
- **Chart.js visualizations** — Radar chart for subject breakdown, bar chart for assessment comparison, CSS grid activity calendar.
- **XSS protection** — All rendered text escaped via esc() function to prevent cross-site scripting.
- **Responsive design** — Card-based layout adapts at 900px and 600px breakpoints for desktop, tablet, and mobile.

### Dashboard Sections

- **Overview Panel** — 4 metric cards (total sessions, completed lessons, overall mastery %, days active) + 30-day activity calendar grid
- **Subject Breakdown** — Chart.js radar chart with 5 axes + subject cards showing name, icon, score, level, and topic count
- **Skill Gap Report** — Sortable table with topics ranked by score (weakest first), color-coded level badges, and actionable recommendations
- **Session History** — Filterable table (by subject, by type) with date, topic, score, and duration. Empty state for new students.
- **Assessment & Progress** — Bar chart comparing subject mastery scores + badge timeline showing earned badges chronologically

### Backend

- **Parent config** — JSON file at data/parent_config.json with PIN and timestamps. Default PIN 0000.
- **5 data aggregation functions** — aggregate_student_overview, aggregate_subject_breakdown, analyze_skill_gaps, build_session_history, build_progression_data
- **4 API endpoints** — /api/parent/login (POST), /api/parent/setup (POST), /api/parent/students (GET), /api/parent/dashboard/{id} (GET)
- **Single dashboard endpoint** — /api/parent/dashboard/{id} returns all 5 sections in one call to minimize frontend API requests

### Acceptance Criteria

- [x] Dashboard accessible via /parent URL with PIN protection
- [x] Shows real-time data aggregated from all student JSON files
- [x] All 5 dashboard sections functional with charts and tables
- [x] Data refreshes when the page is loaded or student is switched
- [x] Works on desktop and tablet browsers (responsive breakpoints)
- [x] Parent can change PIN via /api/parent/setup
- [x] Student selector loads all registered students
- [x] Skill gaps sorted weakest-first with recommendations
- [x] Session history filterable by subject and type
- [x] Empty states render gracefully for students with no data

---

## Feature 7: Multi-Tenancy (Instance per Family)
**Must-Have | Status: Complete**

### What It Does
Admin-provisioned instance isolation allowing each family to have their own independent tutor environment. Each instance gets its own student accounts, parent authentication, diagnostic data, and configuration — enabling monetization through per-family instances.

### Key Components

- **Instance registry** — Central `instances.json` tracking all provisioned instances with IDs, family names, and creation dates
- **Instance directory isolation** — Each instance gets `data/instances/{id}/` with its own students, parent config, feedback, diagnostics, and safety logs
- **Legacy migration** — Automatic non-destructive migration of existing flat data into a `default` instance on first run
- **Instance-scoped parent auth** — Parent PIN validation is per-instance, not global
- **Admin instance creation** — API endpoint for provisioning new family instances
- **Instance-scoped API endpoints** — All parent and student-facing endpoints accept instance_id parameter
- **Instance-aware helper functions** — All 24 data helper functions (load_student, save_student, list_students, get_student_dirs, session_path, load_session, save_session, diagnostic_path, load_diagnostic, save_diagnostic, profile_path, load_profile, save_profile, lesson_dir_for_subject, load_lesson, save_lesson, load_lesson_log, save_lesson_log, practice_dir_for_subject, load_practice, save_practice, load_practice_log, save_practice_log, check_and_award_badges) accept an optional `instance_id` parameter that routes data to the correct instance directory
- **Instance-aware Pydantic models** — All 11 student-facing request models (ChatRequest, DiagnosticStartRequest, DiagnosticAnswerRequest, LessonStartRequest, LessonMessageRequest, PracticeStartRequest, PracticeAnswerRequest, PracticeHintRequest, PracticeEndRequest, StudentCreateRequest, StudentLoginRequest) include `instance_id` field
- **Frontend instance detection** — `index.html` extracts `studentInstanceId` from the URL path (`/f/{id}`) and threads it through `apiUrl()` (query params) and `apiBody()` (POST bodies) for all API calls

### Acceptance Criteria

- [x] Create a new family instance via admin API
- [x] Instance gets isolated directory with all required subdirectories
- [x] Legacy data automatically migrates to default instance
- [x] Parent PIN authentication works per-instance
- [x] Student data is fully isolated between instances
- [x] All existing parent endpoints work with instance scoping
- [x] All student-facing endpoints (chat, diagnostic, lesson, practice) work with instance scoping
- [x] Student login screen shows only students belonging to the current instance
- [x] Diagnostic results are scoped to the correct instance (no false positives from other instances)
- [x] Instance registry tracks all active instances

---

## Feature 8: Platform Customization
**Must-Have | Status: Complete**

### What It Does
Per-instance customization allowing parents to toggle subjects, create custom subjects, set branding, configure grade levels, and enable/disable features.

### Key Components

- **Subject toggles** — Enable or disable any of the 5 master subjects (math, science, ela, social_studies, latin) per instance
- **Custom subjects** — Parents can define new subjects with name, icon (emoji), color, custom topic list, and auto-generated system prompt
- **Branding** — Custom app title and primary accent color applied to student and parent UIs
- **Grade level defaults** — Set per-instance grade level affecting diagnostic prompts and lesson difficulty
- **Feature flags** — Toggle diagnostics, lessons, and practice on/off per instance

### Acceptance Criteria

- [x] Parents can toggle master subjects on/off from the Customization tab
- [x] Parents can create custom subjects with name, icon, color, and topics
- [x] Custom subjects appear in the student UI alongside master subjects
- [x] Branding (title and accent color) applies to student and parent dashboards
- [x] Grade level default is configurable per instance
- [x] Feature flags control which modes are available to students
- [x] Removing a custom subject works without affecting other data

---

## Feature 9: Ad Hoc Diagnostics & Parent Controls
**Must-Have | Status: Complete**

### What It Does
Gives parents the ability to initiate diagnostic assessments for their students and manage diagnostic results, including deleting completed diagnostics to allow re-testing.

### Key Components

- **Schedule diagnostics** — Parent clicks "Start Diagnostic" for any subject; student sees a banner at next login
- **Pending diagnostic banner** — Student UI shows a yellow notification banner with "Start Now" button when a diagnostic is pending
- **Cancel pending** — Parent can cancel a scheduled diagnostic before the student starts it
- **Delete results** — Parent can delete completed diagnostic results to allow re-assessment
- **Status tracking** — Parent dashboard shows per-subject diagnostic status: Completed (with score/date), Pending, or Not Started

### Acceptance Criteria

- [x] Parent can schedule a diagnostic for any subject from the Diagnostics tab
- [x] Student sees pending diagnostic banner on welcome screen
- [x] Student can start the pending diagnostic from the banner
- [x] Parent can cancel a pending diagnostic
- [x] Parent can delete completed diagnostic results (with confirmation)
- [x] Diagnostics tab shows real-time status for all subjects per student
- [x] Re-running a diagnostic for a completed subject works correctly

---

## Feature 10: Feedback Mechanism
**Must-Have | Status: Complete**

### What It Does
A structured feedback collection system with approval workflow. Students and parents can submit feedback (bug reports, feature requests, content issues, general). Student feedback requires parent approval before being visible. Approved feedback can be promoted to platform-level for the admin to review.

### Key Components

- **Student feedback modal** — Button on welcome screen opens a modal with type selector, title, and message fields
- **Parent feedback submission** — Parents submit feedback directly (auto-approved, no review needed)
- **Approval workflow** — Parent reviews student feedback: approve, decline, or promote to platform
- **Platform promotion** — Approved feedback can be promoted to platform-level, visible in the admin dashboard
- **Admin dashboard** — Separate admin page (`/admin`) showing all platform feedback, instance counts, and feedback statistics
- **Feedback types** — Bug report, feature request, content issue, and general feedback with color-coded badges

### Acceptance Criteria

- [x] Student can submit feedback from the welcome screen via feedback button
- [x] Student feedback starts with "pending" status
- [x] Parent can view all instance feedback in the Feedback tab
- [x] Parent can approve or decline student feedback
- [x] Approved feedback can be promoted to platform level
- [x] Parent can submit their own feedback (auto-approved)
- [x] Admin dashboard shows platform feedback with statistics
- [x] Feedback types are color-coded (bug=red, feature=blue, content=yellow, general=gray)

---

## Feature 11: Parent PIN Management
**Important | Week 7–8 | Status: Complete**

### What It Does
Adds a Settings tab to the parent dashboard where parents can manage PINs securely. Parents can change their own PIN, view all student PINs in their family, and reset any student's PIN if forgotten.

### Key Components

- **Parent Settings tab** — New tab in parent dashboard with PIN management interface
- **Change parent PIN** — Form to set a new 4-digit PIN (with confirmation)
- **View student PINs** — Display all student accounts with their current PINs for reference
- **Reset student PIN** — Quick action to reset a student's PIN to a default (e.g., 0000) with confirmation
- **Add Student** — Form in Settings tab to create a new student account with name, 4-digit PIN, and avatar selection (8 emoji options). Validates PIN format and name before creation. Refreshes the student PIN table on success.
- **API endpoints** — `GET /api/instance/{id}/parent/students/with-pins`, `POST /api/instance/{id}/parent/reset-student-pin`, and `POST /api/instance/{id}/parent/add-student`

### Acceptance Criteria

- [x] Parent Settings tab renders in parent dashboard
- [x] Parent can change their own PIN with confirmation
- [x] Parent can view all student PINs in family
- [x] Parent can reset any student's PIN with confirmation dialog
- [x] Parent can add a new student with name, PIN, and avatar from Settings tab
- [x] Add Student validates PIN (must be exactly 4 digits) and name (required)
- [x] Student PIN table refreshes immediately after adding a new student
- [x] All API endpoints return correct data and status codes
- [x] UI updates immediately after PIN changes, resets, or student additions

---

## Feature 12: Path-Based Instance URL Routing
**Important | Week 7–8 | Status: Complete**

### What It Does
Introduces clean, path-based URLs for accessing family instances. Makes sharing and bookmarking family URLs simpler and more professional than query parameters.

### Key Components

- **Student login URL** — `/f/{instance_id}` — Direct entry for students in a specific family
- **Parent dashboard URL** — `/f/{instance_id}/parent` — Parent access for a specific family
- **Legacy fallback** — `?instance=xxx` query params still work for backward compatibility
- **URL routing logic** — Frontend detects path-based IDs and extracts instance context automatically
- **Link generation** — Admin can generate shareable family URLs for easy setup distribution

### Acceptance Criteria

- [x] `/f/{instance_id}` loads student login for that instance
- [x] `/f/{instance_id}/parent` loads parent dashboard for that instance
- [x] Legacy `?instance=xxx` URLs still work
- [x] Instance context persists across page navigations
- [x] Shareable family invite links work correctly

---

## Feature 13: Beta Testing & Remote Access
**Operational | Status: Complete**

### What It Does
Enables remote testing of the Atlas by exposing the local development server via a secure tunnel. Used for beta family testing where a second family can access their own instance from a separate device and location.

### Key Components

- **Cloudflare Tunnel** — `cloudflared tunnel --url http://localhost:8000` creates a temporary public HTTPS URL (e.g., `https://random-words.trycloudflare.com`) that tunnels to the local server. Free, no account required.
- **Three terminal windows** — Required during remote testing: (1) uvicorn server, (2) cloudflared tunnel, (3) general use
- **Beta instance** — Instance `1fb2658dfd1a` ("Beta Family") created via admin API for testing
- **Shareable URLs** — Beta family accesses their instance at `{tunnel_url}/f/1fb2658dfd1a` (student) and `{tunnel_url}/f/1fb2658dfd1a/parent` (parent dashboard)

### Important Notes

- Each `cloudflared` restart generates a new URL — must re-share with beta family after restart
- ngrok is NOT recommended — its `.dev` TLD triggers Chrome's HSTS preload list, causing `ERR_SSL_PROTOCOL_ERROR`
- Parallel development is safe — code changes affect all instances (shared application files), but each instance's data is fully isolated
- The local developer can test both the default instance (`localhost:8000`) and beta instance (`localhost:8000/f/1fb2658dfd1a`) simultaneously

### Setup Steps

1. Install: `brew install cloudflared`
2. Start server: `python3 -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload`
3. Start tunnel: `cloudflared tunnel --url http://localhost:8000`
4. Share the generated URL + instance path with the beta family

---

## Feature 14: Adaptive Learning Engine
**Important | ✅ Complete | Status: Complete**

### What It Does
The intelligence layer that makes the tutor truly personalized. It analyzes patterns in performance data and automatically adjusts the learning path, difficulty, and teaching approach.

### Key Components

- **Spaced repetition** — Topics resurface at optimal intervals to reinforce retention
- **Learning path optimization** — Automatically sequence topics based on prerequisites
- **Difficulty calibration** — Maintain a sweet spot where ~70–80% of problems are answered correctly
- **Teaching style rotation** — If explanations aren't working, try worked examples or problem-first discovery
- **Weekly learning plan** — Auto-generate a suggested study plan based on current gaps and recent progress

### Adaptation Rules

- **IF correct rate > 90% for 3 sessions** — Increase difficulty and introduce next topic
- **IF correct rate < 50% for 2 sessions** — Decrease difficulty, review prerequisites, switch approach
- **IF topic unpracticed 7+ days AND mastery < Proficient** — Queue for spaced repetition
- **IF student consistently uses hints** — Flag for re-teaching with different approach

---

## Feature 15: Periodic Re-Assessment & Growth Tracking
**Important | ✅ Complete**

### What It Does
Auto-scheduled progress checkpoints (default every 2 weeks) that reassess only weak/developing topics, track growth over time, and recalibrate the learning path. Shorter than full diagnostics (6-10 questions), focused on areas below 90% mastery.

### Key Components

- **Auto-scheduled checkpoints** — Configurable interval (1-8 weeks, default 2), with parent override (snooze, trigger now, enable/disable)
- **Focused scope** — Only topics scoring below 90% mastery are tested; mastered topics skipped entirely
- **Growth tracking** — Per-subject timeline showing initial diagnostic → each checkpoint with score deltas
- **Level-up detection** — Celebrates when a topic moves up a mastery tier (e.g., Developing → Proficient)
- **Profile merging** — Checkpoint results merge into existing student profiles, updating mastery scores for all downstream features
- **Student UI** — Blue banner on home screen when checkpoint is due; chat-based flow identical to diagnostics
- **Parent controls** — Analytics tab → Growth Tracking section with schedule settings, snooze, and growth charts
- **XP rewards** — Students earn XP for completing checkpoints, same as diagnostic completion

---

## Feature 16: Schoolwork Upload & Curriculum Integration
**Must-Have | Status: ✅ Complete**

### What It Does
Allows you or your son to upload current school assignments, tests, worksheets, syllabi, and textbook pages. The AI analyzes the uploaded content to identify topics, difficulty level, and curriculum alignment — then weaves that material directly into the tutor's lesson plans.

### Key Components

- **File upload interface** — Drag-and-drop supporting PDFs, images, Word docs, and plain text
- **AI document analysis** — Claude reads uploaded content and extracts subject area, topics, difficulty, question types, and due dates
- **Topic mapping** — Extracted topics matched to the tutor's existing skill map; new topics added automatically
- **Assignment practice mode** — Generate practice problems modeled after the uploaded assignment
- **Curriculum sync** — Syllabus uploads let the tutor anticipate and pre-teach upcoming topics
- **Grade tracking** — Upload graded assignments to record scores and prioritize missed topics

### Supported Upload Types

| Upload Type | Formats | What the Tutor Does |
|-------------|---------|---------------------|
| **Homework** | PDF, image, DOCX | Extracts topics, generates similar practice problems |
| **Tests / Quizzes** | PDF, image, DOCX | Identifies tested skills, creates targeted review |
| **Graded Work** | PDF, image | Records score, flags missed questions, adjusts profile |
| **Syllabus** | PDF, DOCX, TXT | Maps semester topics, enables pre-teaching |
| **Textbook Pages** | PDF, image | Supplements lessons with aligned explanations |

---

## Feature 17: Gamification & Motivation System
**Must-Have | Complete | Status: Complete**

### What It Does
A motivational layer that makes learning feel rewarding and encourages daily usage. Adds game-like elements without distracting from learning.

### Key Components

- **XP system** — Earn XP for diagnostics (50), lessons (40), practice completion (30), correct answers (5-8), streak bonuses (15-30), perfect practice (50), daily login (10), and badge unlocks (20). XP tracked per student with rolling log of last 50 events.
- **10-level progression** — Level 1 Beginner (🌱) → Level 10 Scholar (🎓) with increasing XP thresholds (0, 100, 250, 500, 850, 1300, 1900, 2700, 3800, 5000).
- **Gamification bar** — Prominent XP bar on home screen showing current level icon/name, XP progress toward next level, and daily streak count.
- **Daily streak tracker** — Consecutive days of login calculated from activity_dates. Current and best streak displayed on home screen and profile.
- **Level-up animation** — Full-screen celebratory overlay with bouncing card showing new level icon, name, and "Awesome!" dismiss button.
- **XP toast notifications** — Slide-in green gradient toast in top-right showing "+X XP — Reason" for each XP award event.
- **Profile integration** — Profile hub shows two rows of stats: Level/XP/Streak/Accuracy and Diagnostics/Lessons/Practice/Badges.
- **Practice XP rewards** — Correct answers earn 5 XP (or 8 without hints), 5-streak bonus (15 XP), 10-streak bonus (30 XP), perfect practice bonus (50 XP).

### Technical Details
- Backend: `XP_REWARDS` constants, `LEVELS` array, `award_xp()` helper, `get_level_for_xp()`, `get_next_level()`, `get_daily_streak()` functions in app.py
- XP wired into: student login (daily), diagnostic completion, lesson completion, practice answers, practice completion, badge unlocks
- Frontend: `updateGamificationBar()`, `showXPToast()`, `showLevelUpAnimation()`, `handleXPResponse()`, `refreshStudentStats()` functions in index.html
- `/api/student/stats/{student_id}` and `/api/student/login` endpoints return full XP/level/streak data

---

## Feature 18: Socratic Mode
**Important | Complete | Status: Complete**

### What It Does
A parent-controlled teaching mode where the tutor guides students to discover answers through questions rather than giving direct explanations. When enabled, the tutor uses the Socratic method across chat tutoring and structured lessons.

### Key Components

- **Per-student setting** — Stored in each student's `preferences.socratic_mode` field. Defaults to ON for all students. Parents toggle it from the Customization tab, and the setting is saved immediately per student.
- **Socratic system prompt** — A `SOCRATIC_PROMPT` constant appended to chat and lesson system prompts when enabled. Contains 9 rules governing the tutor's behavior: never give direct answers, respond with guiding questions, give smallest possible hints, break complex problems into smaller questions, etc.
- **Chat integration** — The `/api/chat` endpoint checks `is_socratic_mode()` for the logged-in student and appends the Socratic prompt to the subject's system prompt before calling Claude.
- **Lesson integration** — The `build_lesson_system_prompt()` function accepts `student_id` and appends the Socratic prompt when enabled. The 5-step lesson structure is preserved, but the tutor's approach within each step shifts to guided questioning.
- **Scoped to chat and lessons only** — Diagnostics (which need to assess answers) and practice (which needs to confirm right/wrong) are unaffected by Socratic mode.
- **Parent Customization tab** — A new "Teaching Mode" section appears below Feature Toggles, showing the currently selected student's name and a Socratic Mode toggle with description. Changes are saved immediately via `PUT /api/instance/{id}/student/preferences`.
- **Parent-authenticated preferences endpoint** — `PUT /api/instance/{id}/student/preferences` accepts a parent PIN, student ID, and preferences dict. Merges new preferences into existing ones (doesn't replace).

### Technical Details
- `is_socratic_mode(student_id, instance_id)` helper function reads student preferences, defaults to True
- `SOCRATIC_PROMPT` is ~500 chars of detailed behavioral instructions for Claude
- Preferences stored in student JSON: `preferences: { socratic_mode: true/false }`
- Frontend toggle calls the preferences endpoint on every change (no "Save" button needed)
- Dashboard response now includes `student.preferences` for the parent frontend to read

---

## Feature 19: Voice Input & Text-to-Speech
**Important | Status: ✅ Complete**

### What It Does
Allows your son to speak to the tutor instead of typing, and hear responses read aloud. Uses the Web Speech API built into Chrome — no extra cost.

### Key Components

- **Microphone button** — Click to start voice input. Speech transcribed to text in real-time.
- **Read-aloud button** — Each tutor response has a speaker icon. Auto-read option in settings.

---

## Feature 20: Visual Math Rendering
**Important | Complete | Status: Complete**

### What It Does
Renders math expressions beautifully using KaTeX so fractions, exponents, square roots, and equations display as proper mathematical notation instead of plain text. Also adds lightweight Markdown rendering (bold, italic, lists) for all tutor responses.

### Key Components

- **KaTeX integration** — CDN-loaded KaTeX v0.16.11 renders both inline (`$...$`) and display (`$$...$$`) LaTeX math expressions. Also supports `\(...\)` and `\[...\]` delimiters.
- **Lightweight Markdown renderer** — Custom `renderFormattedContent()` function in `index.html` parses bold (`**`), italic (`*`), inline code, numbered lists, and bullet lists into HTML. No external Markdown library needed.
- **Math formatting system prompts** — `MATH_FORMATTING_RULES` constant in `app.py` appended to all Math and Science system prompts, instructing Claude to use LaTeX notation for all mathematical expressions.
- **XSS-safe rendering** — HTML is escaped before rendering; only tutor (assistant) messages use `innerHTML`; user messages remain `textContent` for safety.

### Acceptance Criteria
- [x] KaTeX CDN loads on page and renders inline/display math
- [x] Quadratic formula, fractions, exponents, square roots all render correctly
- [x] Bold, italic, numbered lists render in tutor responses
- [x] User messages remain plain text (no XSS risk)
- [x] Math/Science system prompts include LaTeX formatting instructions
- [x] Non-STEM subjects (ELA, Social Studies, Latin) do not receive math formatting rules

---

## Feature 21: Quick Quiz & Flashcard Mode
**Important | Complete | Status: Complete**

### What It Does
A dedicated study mode accessible from the sidebar with two AI-powered review activities: flashcards and timed quizzes. Claude generates personalized content calibrated to the student's diagnostic profile.

### Key Components

- **Study picker** — Sidebar nav button ("🃏 Study") opens a topic/mode selector. Students choose between flashcards and quiz, then pick a topic from their diagnostic results
- **Flashcard interface** — CSS 3D flip animation (perspective + rotateY + backface-visibility). Cards show question on front, answer on back. "Got It" and "Study Again" buttons; missed cards are re-queued for additional review
- **AI-generated decks** — Claude generates 10 flashcards per session, calibrated to the student's diagnostic level on each topic. Supports LaTeX math rendering
- **Quick quiz mode** — Timed multiple-choice quiz with 8 questions, 4 choices each. Instant feedback with explanations after each answer. Progress bar and running score displayed throughout
- **XP rewards** — Flashcard completion: 20 XP. Quiz completion: 25 XP. Perfect quiz bonus: +40 XP. Badges checked after each session
- **Summary screens** — Both modes show completion stats (score, time, percentage) with options to retry, change topic, or return home

### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/study/flashcards` | POST | Generate AI flashcards for a topic |
| `/api/study/quiz` | POST | Generate multiple-choice quiz questions |
| `/api/study/complete` | POST | Record completion and award XP |

### Technical Details
- Flashcard generation uses regex JSON extraction from Claude response for robust parsing
- Quiz questions include distractors calibrated by student level — easier for "Needs Work", harder for "Strong"
- Timer runs via setInterval, displayed as MM:SS in quiz header
- No Socratic mode overlay for study activities (direct answers are appropriate for review)
- Study mode only unlocks after diagnostic completion (requires topic data for the picker)

---

## Feature 22: Study Timer & Session Goals
**Important | Status: ✅ Complete**

### What It Does
A structured study session system with a Pomodoro-style timer (25 min study, 5 min break) and session targets. Helps build study discipline for high school preparation.

### Key Components

- **Study timer** — Configurable Pomodoro timer with visual countdown and optional audio chime
- **Session goals** — Set targets before starting. Progress bar tracks completion. Completing goals earns bonus XP.
- **Daily study log** — Automatic logging of total study time, subjects covered, and goals completed

---

## Feature 23: Product Tour & Help Section
**Must-Have | Complete | Status: Complete**

### What It Does
A guided onboarding experience for first-time users and a persistent help section for ongoing reference. Ensures new families can immediately understand what the tutor offers and how to use every feature — critical before taking the product public.

### Key Components

- **First-time student tour** — 8-step overlay walkthrough triggered on first student login. Highlights: home screen, subject buttons, navigation (Home, Results, Lessons, Practice), diagnostic grid, and help FAB. Skippable with Back/Next navigation and "Skip Tour" option. Remembered per instance via localStorage (`tour_seen_student_{instanceId}`). Always replayable from help menu.
- **First-time parent tour** — 8-step overlay walkthrough triggered on first parent login. Covers: dashboard header, student selector, all 5 tabs (Overview, Diagnostics, Customization, Feedback, Settings), and help FAB. Remembered per instance via localStorage (`tour_seen_parent_{instanceId}`).
- **Help FAB (?)** — Fixed-position floating action button (bottom-right) on both student and parent views. Opens a 3-option menu: "Take the Tour" (replays tour), "Help & FAQ" (inline help page), and "Training Guide" (opens /guide in new tab). Appears after login, hides on logout.
- **Student Help & FAQ** — Inline panel with 7 sections: Getting Started, Diagnostics, Lessons, Practice, Badges, Feedback, and FAQ with common questions.
- **Parent Help & FAQ** — Inline panel within dashboard with 6 sections: Dashboard Overview, Diagnostics, Customization, Feedback, Settings, and FAQ with parent-specific questions.
- **Training guide** — Full HTML page served at `/guide` with 13 sections covering the entire product. Includes table of contents, step-by-step instructions, callout tips, and troubleshooting. Print-friendly and mobile-responsive. Accessible from help menu on both student and parent views.

### Technical Details
- Tour system uses DOM overlay with box-shadow cutout for highlighting, positioned tooltips, and CSS animations
- No external libraries — pure vanilla JS and CSS
- Tour state persisted in localStorage per-instance for both student and parent
- `/guide` route added to app.py serving `static/guide.html`
- Help FAB and menu added to both `static/index.html` and `static/parent.html`

---

## Feature 24: Onboarding Intake Form
**Must-Have | Complete | Status: Complete**

### What It Does
A guided self-service setup wizard that lets new families create their own Atlas instance. Captures family info, creates the first student, configures subjects, and sets learning goals — all in a polished 4-step flow served at `/setup`.

### Key Components

- **4-step intake wizard** — Beautiful card-based form with animated step transitions and progress bar: Welcome (family name, email, parent PIN), Student Info (name, PIN, grade, avatar), Subjects (toggle subjects on/off), Goals (learning goal categories + free-text notes).
- **Smart instance configuration** — Creates instance with selected subjects enabled, sets grade level, stores learning goal categories and notes in instance config under `customization.learning_goals`.
- **Parent PIN setup** — Parent sets their own PIN during onboarding (no default 0000).
- **First student creation** — Student account created as part of the flow with name, PIN, grade, avatar, and all data subdirectories.
- **"Get Started" button** — Added to the student login screen (`index.html`) below the login tabs. Links to `/setup` for new families.
- **Success screen** — After setup, shows direct links to the new instance's student view (`/f/{instance_id}`) and parent dashboard (`/f/{instance_id}/parent`).
- **Validation** — All steps validated before advancing: family name required, PINs must be 4 digits, student name required, at least one subject selected.

### Intake Form Steps

| Step | What It Captures | How It's Used |
|------|-----------------|---------------|
| **Welcome** | Family name, parent email, parent PIN | Creates instance, sets parent PIN |
| **Student Info** | Name, PIN, grade, avatar | Creates first student account |
| **Subjects** | Which subjects to enable | Configures `enabled_subjects` on instance |
| **Goals** | Learning goal categories, free-text notes | Stored in `customization.learning_goals` for future adaptive engine |

### Technical Details
- Frontend: `static/setup.html` — standalone page with inline CSS/JS, PIN auto-advance, animated transitions
- Backend: `POST /api/setup` — validates input, calls `create_instance()`, overwrites parent PIN, creates student, returns instance ID
- Page route: `GET /setup` served from app.py
- Invite link integration added in Feature 13 — setup.html detects `/invite/{code}` from URL, validates the code, and passes it in the setup payload

---

## Feature 13: Family Invite Links
**Must-Have | Complete | Status: Complete**

### What It Does
Allows existing families to generate shareable invite links that let new families set up their own Atlas instance. Invite links support usage limits (max uses and expiration) and are managed from the parent dashboard. This enables organic growth through word-of-mouth sharing.

### Key Components

- **Invite creation** — Parents generate invite links from the Invites tab on the parent dashboard. Each invite has an optional label, configurable max uses (unlimited, 1, 3, 5, 10, or 25), and expiration period (never, 1, 3, 7, 14, or 30 days).
- **Invite link URL** — Links use the format `/invite/{10-char-hex-code}` which serves the setup page with invite context. The setup page detects the invite code from the URL path and validates it on load.
- **Invite validation** — On page load, setup.html calls `/api/invites/validate/{code}` to check validity. Valid invites show a banner with the inviting family's name. Invalid/expired/revoked invites show an error with a "Set Up Without Invite" fallback.
- **Usage tracking** — Each time an invite is used to create a new instance, the use count increments and the new family's info is recorded in `used_by`. The invite list in the parent dashboard shows real-time usage.
- **Invite management** — Parent dashboard Invites tab shows all invites with status badges (Active, Revoked, Expired, Max Reached), copy-link buttons, revoke buttons, and a list of families who used each invite.
- **Global invite storage** — Invites stored in `data/invites.json` (not per-instance) to allow cross-instance lookup during validation.
- **Setup integration** — The `/api/setup` endpoint accepts an optional `invite_code` field. If provided, it validates the invite before creating the instance and records usage after successful creation.

### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/invites/create` | POST | Create a new invite (requires parent PIN) |
| `/api/invites/list` | GET | List invites for an instance (requires parent PIN) |
| `/api/invites/revoke` | POST | Revoke an invite (requires parent PIN) |
| `/api/invites/validate/{code}` | GET | Validate an invite code (public) |
| `/invite/{code}` | GET | Serve setup page for invite link |

### Technical Details
- Invite codes are 10-character hex strings generated with `secrets.token_hex(5)`
- Invites stored globally in `data/invites.json` with atomic write (tmp + rename)
- Setup page (`static/setup.html`) uses async IIFE on load to detect `/invite/{code}` in URL path
- Invalid invites show specific error titles: "Invite Expired", "Invite Revoked", "Invite Limit Reached"
- Parent dashboard Invites tab added with create form, link display area, and active invite list

---

## Feature 25: Grade Scaling (6–12 Support)
**Nice-to-Have | ✅ Complete | Status: Complete**

### What It Does
Transforms the tutor from an 8th-grade-only tool into a multi-grade platform supporting grades 6 through 12. Currently, most system prompts hardcode "8th grader" regardless of the student's actual grade setting. This feature makes all AI prompts, topic lists, content safety rules, and subject catalogs dynamically adapt to the student's grade level so the tutor can serve middle schoolers through high school graduation.

### Key Components

- **Dynamic prompt injection** — Replace all hardcoded "8th grader" references in lesson prompts (line ~1624), diagnostic prompts (line ~1667), and practice prompts (line ~1731) with the student's actual grade variable. Flashcards and quizzes already use `{grade}th grade` and serve as the template for this change.
- **Grade-aware content safety rules** — Update `CONTENT_SAFETY_RULES` (currently hardcoded to "8th grader, ages 12–14") to dynamically set age range based on grade: Grade 6 → ages 10–12, Grade 7 → ages 11–13, Grade 8 → ages 12–14, Grade 9 → ages 13–15, Grade 10 → ages 14–16, Grade 11 → ages 15–17, Grade 12 → ages 16–18.
- **Grade-specific topic lists** — Expand the `SUBJECTS` dictionary so each subject has grade-appropriate topics. For example, Math Grade 6 covers ratios, basic geometry, and intro to expressions; Grade 8 covers pre-algebra; Grade 11 covers pre-calculus and trigonometry. Options: (a) maintain static topic lists per grade, or (b) let Claude dynamically select grade-appropriate topics within broader subject areas.
- **Grade progression UI** — Add a control in the parent Settings tab to advance a student's grade level. When the parent updates the grade, all future lessons, diagnostics, and practice sessions use the new grade's prompts and topics.
- **Tutor persona adaptation** — Adjust the AI's communication style by grade: concrete examples and simple vocabulary for Grades 6–7, moderate scaffolding for Grade 8, more academic rigor and independent thinking for Grades 11–12.
- **Backward compatibility** — Existing students with Grade 8 see no change. The default grade remains 8 for new students. All existing data (diagnostics, lessons, practice) remains valid regardless of grade changes. The onboarding intake form grade selector will be expanded to include grades 6 and 7.

### Technical Details
- Primary changes in `app.py`: `build_lesson_system_prompt()`, `build_diagnostic_system_prompt()`, `build_practice_system_prompt()`, and `CONTENT_SAFETY_RULES`
- Student grade already stored in student JSON (`grade` field) — no schema changes needed
- Parent dashboard already has student edit capability — grade selector extension is straightforward
- Topic expansion may require a `SUBJECTS_BY_GRADE` dictionary or a Claude-powered topic generation approach
- Estimated scope: ~200 lines in app.py, ~50 lines in parent.html

---

## Feature 26: ADD/ADHD Adaptability
**Nice-to-Have | Status: Planned**

### What It Does
Adds a suite of parent-configurable accommodations that make the tutor more effective for students with ADD, ADHD, or other attention and executive-function challenges. These features leverage what the tutor already does well (gamification, Socratic questioning, short flashcard sessions) and add targeted support for focus, pacing, and cognitive load management.

### Key Components

- **Chunking and pacing controls** — Parent-configurable option to break lessons into shorter sub-steps, reduce the number of practice questions per session, and insert break reminders after a configurable number of minutes. The lesson's 5-step structure can optionally split each step into micro-steps (e.g., "Read this paragraph, then we'll discuss").
- **Visual progress cues** — Enhanced progress indicators that are always visible: prominent progress bars showing exact position in lesson/practice, countdown indicators ("3 more questions!"), and time-remaining displays. These cues reduce anxiety about "how much is left" and help maintain engagement.
- **Reduced cognitive load mode** — A toggle that simplifies the UI to show one thing at a time. In practice mode, only the current question is visible (no stats bar clutter). In lessons, each micro-step is isolated. Sidebars and navigation are minimized. This reduces visual distractions.
- **Refocus prompts** — Detect extended inactivity (configurable idle timeout, e.g., 2–5 minutes with no input) and display a gentle nudge: "Still thinking? Here's a hint to get started..." or "Want to take a quick break? Press Enter when you're ready." These are non-punitive and encouraging.
- **Session length presets** — Parent-configurable maximum session durations (15, 25, 45, or 60 minutes) with optional Pomodoro-style breaks (5-minute break every 25 minutes). When time is nearly up, the tutor wraps up gracefully rather than cutting off mid-question. A visible countdown timer helps students self-regulate.
- **Multi-modal reinforcement** — Prompt Claude to include worked examples, visual analogies ("think of fractions like pizza slices"), and step-by-step breakdowns alongside text explanations. Students who struggle with processing speed benefit from seeing the same concept explained multiple ways.
- **Positive reinforcement frequency** — Parent-configurable encouragement interval. Options: every question, every 3 questions, or minimal. For students who need more frequent positive feedback, the tutor inserts encouraging remarks ("Great effort!", "You're making progress!") more often. This uses a system prompt modifier rather than hardcoded messages.

### Technical Details
- New student preference fields: `focus_mode` (boolean), `chunk_size` (small/medium/large), `session_max_minutes` (number), `break_interval` (number), `idle_timeout_seconds` (number), `reinforcement_frequency` (every/moderate/minimal)
- Parent Customization tab gets a new "Learning Accommodations" section with per-student toggles and sliders
- System prompt composition gains a new overlay (similar to Socratic mode): when focus_mode is enabled, additional instructions are injected telling Claude to use shorter paragraphs, more frequent check-ins, and multi-modal explanations
- Frontend idle detection via `setInterval` checking time since last input event
- Session timer reuses the existing quiz timer pattern but applies globally to all modes
- Estimated scope: ~150 lines in app.py (prompt overlays, preference endpoints), ~300 lines in index.html (timer, idle detection, reduced-load UI), ~100 lines in parent.html (accommodation controls)

---

## Feature 27: Parent Safety Transparency
**Must-Have | ✅ Complete | Status: Complete**

### What It Does
Makes the tutor's content safety rules fully visible and reviewable by parents, and surfaces safety event data in the parent dashboard. Currently, content safety rules exist in the backend code (`CONTENT_SAFETY_RULES`, `INJECTION_PATTERNS`, `BLOCKED_TOPICS`) and a safety log API endpoint exists (`/api/safety-log`), but neither is accessible from the parent UI. This feature bridges that gap.

### What's Already Done (Documentation Only)
As of March 15, 2026, the content safety rules have been documented in plain language in three places:
- **Parent Help & FAQ** — A "Content Safety" card listing all 9 AI content rules plus pre-screening protections
- **Training Guide** — Section 14 "Content Safety" with AI content rules, pre-screening protections, and logging info
- **Student Help** — Existing FAQ entry about safety filters

### What Still Needs to Be Built

- **Safety Log tab in parent dashboard** — A new tab (or sub-section of an existing tab) that displays the safety event log. Shows blocked events with timestamp, student name, event type (injection attempt or blocked topic), and the trigger pattern. Paginated or scrollable. Calls the existing `/api/safety-log` endpoint with instance scoping.
- **Conversation log viewer** — Allow parents to browse per-student conversation logs from the dashboard. Each student already has a `conversation_log.jsonl` file. The viewer would show recent turns with timestamps, student messages, and tutor responses. Searchable and filterable by subject and date.
- **Safety summary on Overview tab** — A small card on the parent dashboard Overview showing: total safety events (last 30 days), most recent event timestamp, and a link to the full Safety Log tab.
- **Email/notification option** — Optional parent notification when a safety event is triggered (future enhancement, depends on email infrastructure).

### Technical Details
- Safety log API already exists at `/api/safety-log` — needs instance-scoping and parent PIN auth
- Conversation logs stored per-student at `data/instances/{id}/students/{sid}/conversation_log.jsonl`
- New endpoint needed: `/api/instance/{id}/parent/safety-log` (PIN-protected, instance-scoped)
- New endpoint needed: `/api/instance/{id}/parent/conversation-log/{sid}` (PIN-protected, paginated)
- Frontend: new tab or section in parent.html (~150 lines for safety log UI, ~200 lines for conversation viewer)
- Estimated scope: ~100 lines in app.py, ~350 lines in parent.html

---

## Testing Log

All automated tests completed on **March 4, 2026**. Tests cover API endpoint validation and Chrome browser UI verification.

### API Endpoint Tests (59/59 Passing)

All 61 API endpoints tested via curl. Every endpoint returned expected data structures and status codes. Includes 15 core endpoints (tutor, diagnostic, lesson), 6 practice endpoints, 8 student account endpoints, 2 content safety endpoints, 4 parent dashboard endpoints, 2 parent PIN management endpoints, 25 multi-tenancy and customization endpoints.

| Endpoint | Method | Status | Notes |
|----------|--------|--------|-------|
| /api/students | GET | Pass | Returns list of all student accounts |
| /api/student/{id} | GET | Pass | Returns student profile with name, grade, avatar |
| /api/student/create | POST | Pass | Creates new student account, returns student_id |
| /api/student/login | POST | Pass | Authenticates with PIN, returns student_id and profile |
| /api/student/update | POST | Pass | Updates student profile (name, grade, avatar) |
| /api/student/stats/{id} | GET | Pass | Returns student statistics (diagnostics, lessons, practice, accuracy) |
| /api/student/{id}/badges | GET | Pass | Returns list of earned badges with award dates |
| /api/student/migrate | POST | Pass | Migrates legacy flat data into student-namespaced directories |
| /api/subjects | GET | Pass | Returns all 5 subjects with topics, icons, profile status |
| /api/sessions | GET | Pass | Returns session list with message counts (student_id filtered) |
| /api/session/{subject} | GET | Pass | Loads existing conversation history for student |
| /api/diagnostic/results | GET | Pass | Returns per-topic scores and levels for all subjects (student_id filtered) |
| /api/diagnostic/results/{sub} | GET | Pass | Returns single-subject profile (student_id filtered) |
| /api/lesson/recommended/{sub} | GET | Pass | Returns weakest topic with reasoning (student_id filtered) |
| /api/lesson/active/{subject} | GET | Pass | Returns active lesson or has_active: false (student_id filtered) |
| /api/lesson/log/{subject} | GET | Pass | Returns lesson history array (student_id filtered) |
| /api/lesson/start | POST | Pass | Creates lesson, calls Claude, returns first message with step (student_id) |
| /api/lesson/message | POST | Pass | Sends message, returns response with step progression (student_id) |
| /api/diagnostic/start | POST | Pass | Starts diagnostic, returns first question (student_id) |
| /api/diagnostic/answer | POST | Pass | Processes answer, advances or completes diagnostic (student_id) |
| /api/diagnostic/reset/{sub} | POST | Pass | Clears diagnostic state (student_id) |
| /api/session/{sub}/clear | POST | Pass | Clears tutor session (student_id) |
| /api/chat | POST | Pass | Sends tutor message, returns response (student_id threaded) |
| /api/practice/start | POST | Pass | Starts practice session, returns first question (student_id) |
| /api/practice/answer | POST | Pass | Submits answer, returns feedback with streak and difficulty (student_id) |
| /api/practice/hint | POST | Pass | Returns escalating hints (tier 1→2→3) (student_id) |
| /api/practice/active/{subject} | GET | Pass | Returns active practice session or has_active: false (student_id) |
| /api/practice/log/{subject} | GET | Pass | Returns practice history array with stats (student_id) |
| /api/practice/end | POST | Pass | Ends session early, returns final stats summary (student_id) |
| /api/student/{id}/conversation-log | GET | Pass | Returns recent conversation log entries for parent review |
| /api/safety-log | GET | Pass | Returns recent safety events (blocked topics, injection attempts) |
| /api/parent/login | POST | Pass | Validates parent PIN, returns status (401 on wrong PIN) |
| /api/parent/setup | POST | Pass | Changes parent PIN (requires current PIN verification) |
| /api/parent/students | GET | Pass | Lists all students with diagnostic counts (PIN query param) |
| /api/parent/dashboard/{id} | GET | Pass | Returns all 5 dashboard sections in one call (PIN query param) |
| /api/admin/instance/create | POST | Pass | Creates new family instance with isolated directory |
| /api/admin/instances | GET | Pass | Lists all provisioned instances with metadata |
| /api/instance/{id} | GET | Pass | Returns instance details and configuration |
| /api/instance/{id}/parent/login | POST | Pass | Instance-scoped parent PIN authentication |
| /api/instance/{id}/parent/setup | POST | Pass | Change parent PIN for specific instance |
| /api/instance/{id}/parent/students | GET | Pass | Lists students within instance (PIN auth) |
| /api/instance/{id}/parent/dashboard/{sid} | GET | Pass | Instance-scoped parent dashboard data |
| /api/subjects/catalog | GET | Pass | Returns master subject catalog |
| /api/instance/{id}/config | PUT | Pass | Updates instance customization settings |
| /api/instance/{id}/subjects/custom | POST | Pass | Adds custom subject to instance |
| /api/instance/{id}/subjects/custom/{key} | DELETE | Pass | Removes custom subject from instance |
| /api/instance/{id}/subjects | GET | Pass | Returns enabled subjects for instance |
| /api/instance/{id}/parent/diagnostic/schedule/{sid}/{subj} | POST | Pass | Schedules diagnostic for student |
| /api/instance/{id}/parent/diagnostic/cancel/{sid}/{subj} | POST | Pass | Cancels pending diagnostic |
| /api/instance/{id}/parent/diagnostic/delete/{sid}/{subj} | POST | Pass | Deletes diagnostic results |
| /api/instance/{id}/parent/diagnostic/status/{sid} | GET | Pass | Returns per-subject diagnostic status |
| /api/student/pending-diagnostics/{sid} | GET | Pass | Returns list of pending diagnostics for student |
| /api/instance/{id}/student/feedback | POST | Pass | Student submits feedback (pending status) |
| /api/instance/{id}/student/{sid}/feedback | GET | Pass | Returns student's own feedback |
| /api/instance/{id}/parent/feedback | POST | Pass | Parent submits feedback (auto-approved) |
| /api/instance/{id}/parent/feedback | GET | Pass | Lists all instance feedback |
| /api/instance/{id}/parent/feedback/{fid} | PUT | Pass | Approve/decline student feedback |
| /api/admin/feedback | GET | Pass | Lists all platform-level feedback |
| /api/admin/feedback/stats | GET | Pass | Returns feedback statistics by type |
| /api/instance/{id}/parent/students/with-pins | GET | Pass | Lists all students with their PINs for a family |
| /api/instance/{id}/parent/reset-student-pin | POST | Pass | Resets a student's PIN to default and returns new PIN |

### Chrome Browser Tests (80/80 Passing)

80 UI tests completed in Chrome covering rendering, navigation, lesson flow, practice mode, mode switching, student accounts, content safety, parent dashboard, multi-tenancy, customization, diagnostics, feedback, parent PIN management, and path-based routing.

| Test | Status | Details |
|------|--------|---------|
| Home screen renders | Pass | All 3 sections visible: Diagnostics, Lessons, Tutoring |
| Diagnostic badges | Pass | Math shows Completed (green), others show Take Assessment (blue) |
| Lesson card visibility | Pass | Math Lesson card appears only with completed diagnostic |
| Sidebar navigation | Pass | Home, Diagnostic Results, Lessons buttons switch panels correctly |
| Recent Sessions sidebar | Pass | Shows Math (2 messages), Science (2 messages) |
| Lesson picker — recommended topic | Pass | Shows Functions & Graphing — scored 70% |
| Lesson picker — topic grid | Pass | All 6 Math topics with color-coded score badges |
| Lesson picker — lesson history | Pass | Shows Functions & Graphing — In Progress — 3/3/2026 |
| Lesson picker — resume banner | Pass | Continue: Functions & Graphing — Step 2 of 5 |
| Start lesson flow | Pass | Recommended topic opens chat with step progress bar |
| Step progress bar | Pass | Step 1 Hook highlighted green on lesson start |
| Lesson Hook content | Pass | Personalized — references 85% linear equations score |
| Send lesson message | Pass | User bubble appears, tutor responds with next content |
| Step advancement | Pass | Progress bar shows Steps 1 and 2 filled after response |
| Step 2 Concept content | Pass | Formal definitions, function machine metaphor, examples |
| Resume lesson | Pass | Restores all messages, correct step, (Resumed) header |
| Recommended topic adapts | Pass | After Functions lesson, recommends Linear Equations |
| Navigate Home from lesson | Pass | Home renders, no lesson progress bar leaking |
| Tutor mode | Pass | Loads Math conversation, 8th Grade Tutor header, no bars |
| Tutor mode header buttons | Pass | View Results and New Session buttons present |
| Diagnostic Results page | Pass | Math: 6 topics with scores; others: Take it now links |
| Mode switching — progress bars | Pass | Lesson bar only in lesson, diag bar only in diag |
| Mode switching — panels | Pass | Panels properly show/hide across all modes |
| Practice Exercises on home | Pass | Practice section visible on home with Math Practice card |
| Practice nav button | Pass | Practice button appears in sidebar for subjects with diagnostics |
| Practice picker — topic grid | Pass | All 6 Math topics with diagnostic score badges and color coding |
| Practice picker — recommended topic | Pass | Weakest topic highlighted as recommended |
| Practice picker — history section | Pass | Practice history shows completed sessions |
| Practice session — stats bar | Pass | Stats bar shows streak, questions, correct, accuracy, difficulty |
| Practice session — hint button | Pass | Hint button visible with 3 hints remaining counter |
| Practice session — difficulty badge | Pass | Color-coded badge: green=easy, yellow=medium, red=hard |
| Login screen renders | Pass | Student cards displayed with name, avatar, and grade for each account |
| PIN pad interaction | Pass | 4-digit PIN entry with dot masking, backspace, and submit button |
| PIN authentication | Pass | Correct PIN logs in; wrong PIN shows red error and shakes |
| Personalized sidebar | Pass | Sidebar shows student name and grade (e.g. Alex Jr. · 8th Grade) |
| Profile Hub — stats | Pass | Shows diagnostics taken, lessons, practice sessions, and accuracy |
| Profile Hub — badges | Pass | Badge grid displays earned badges with icons and locked placeholders |
| Profile Hub — Edit Profile | Pass | Edit Profile button visible; inline name/avatar editing available |
| Logout flow | Pass | Logout button clears state and returns to student login screen |
| Create Account form | Pass | Name, PIN, avatar picker (20 emojis), grade selector all functional |
| Create Account — new student | Pass | New student appears on login screen with correct avatar and grade |
| Data isolation — new student | Pass | Newly created student sees clean slate: 0 diagnostics, 0 lessons |
| Data isolation — existing student | Pass | Returning student retains prior data (diagnostics, sessions) |
| Safety — blocked topic rejected | Pass | Harmful content request returns safe redirect, does not reach Claude |
| Safety — injection attempt caught | Pass | Prompt injection patterns detected and blocked (15 patterns) |
| Safety — normal message passes | Pass | Academic questions pass safety check and reach Claude normally |
| Safety — system prompt hardened | Pass | All 4 prompt types include CONTENT_SAFETY_RULES |
| Safety — conversation logging | Pass | Chat turns logged to student conversation_log.jsonl |
| Safety — event logging | Pass | Blocked events logged to data/safety_logs/ with timestamps |
| Parent login screen renders | Pass | PIN entry pad with 4-digit input, keyboard support, and submit button |
| Parent PIN authentication | Pass | Valid PIN loads dashboard; invalid PIN shows error message |
| Parent dashboard — student selector | Pass | Dropdown lists all students; switching reloads dashboard data |
| Parent dashboard — overview panel | Pass | 4 metric cards (sessions, lessons, mastery, days active) + activity calendar |
| Parent dashboard — subject breakdown | Pass | Radar chart with 5 axes + subject cards with scores, levels, and icons |
| Parent dashboard — skill gap report | Pass | Sortable table with topics ranked by score, color-coded level badges |
| Parent dashboard — session history | Pass | Filterable table (by subject, by type) with date, topic, score, duration |
| Parent dashboard — progress section | Pass | Bar chart comparing subject scores + badge timeline with dates |
| Parent dashboard — responsive design | Pass | Layout adapts at 900px and 600px breakpoints |
| Parent dashboard — empty states | Pass | Graceful handling when student has no data for a section |
| Parent dashboard — Diagnostics tab | Pass | Tab renders with subject cards showing status (completed/pending/not started) |
| Parent dashboard — schedule diagnostic | Pass | Start Diagnostic button triggers pending state |
| Parent dashboard — delete diagnostic | Pass | Delete Results shows confirmation, removes diagnostic data |
| Parent dashboard — Customization tab | Pass | Subject toggles, custom subject form, branding fields render |
| Parent dashboard — custom subject creation | Pass | Form creates custom subject with name, icon, color, topics |
| Parent dashboard — branding settings | Pass | App title and accent color inputs save to instance config |
| Parent dashboard — Feedback tab | Pass | Feedback list with filter sub-tabs (All/Pending/Approved/Declined) |
| Parent dashboard — feedback approval | Pass | Approve/decline buttons update feedback status |
| Parent dashboard — promote feedback | Pass | Promote button copies feedback to platform level |
| Student — pending diagnostic banner | Pass | Yellow banner appears when parent schedules a diagnostic |
| Student — feedback button | Pass | Send Feedback button opens modal on welcome screen |
| Student — feedback modal | Pass | Modal with type selector, title, message fields, and submit |
| Admin dashboard renders | Pass | Instance grid, feedback list, and stats load correctly |
| Admin dashboard — platform feedback | Pass | Shows promoted feedback with type badges and instance attribution |
| Parent dashboard — Settings tab | Pass | Settings tab renders with parent PIN management options |
| Parent dashboard — Change parent PIN | Pass | Form allows entering new 4-digit PIN with confirmation |
| Parent dashboard — View student PINs | Pass | Table displays all students with their current PINs |
| Parent dashboard — Reset student PIN | Pass | Reset button shows confirmation dialog and updates PIN to default |
| Path-based URL — student login | Pass | `/f/{instance_id}` loads student login for that instance |
| Path-based URL — parent dashboard | Pass | `/f/{instance_id}/parent` loads parent dashboard for that instance |
| Path-based URL — legacy fallback | Pass | `?instance=xxx` query params still work as fallback routing |

---

## Recommended User Tests

These tests require real interaction with the Claude API or browser input that could not be fully automated. Run through these manually to verify end-to-end functionality.

### Priority 1 — Core Lesson Flow

- [ ] **Complete a full 5-step lesson.** Start a Math lesson on any topic and go through all 5 steps (Hook → Concept → Guided Practice → Independent Practice → Wrap-up). Verify the progress bar fills all 5 steps and the input disables with "Lesson complete!"
- [ ] **Lesson completion updates history.** After completing a lesson, go back to the lesson picker and verify the lesson shows a green dot and "Completed" in the history section.
- [ ] **Start a second lesson on a different topic.** After completing one lesson, start another. Verify the recommended topic updates (should skip completed/in-progress topics).
- [ ] **End Lesson button mid-lesson.** Start a lesson, interact for a couple steps, then click End Lesson. Confirm the dialog appears and you return to the lesson picker.

### Priority 2 — Practice Engine

- [ ] **Start a practice session.** Select Math, pick any topic from the practice picker, and verify a question appears with the stats bar showing.
- [ ] **Answer questions correctly.** Answer 3+ questions correctly in a row. Verify streak counter increments and difficulty may increase.
- [ ] **Use all 3 hint tiers.** On a practice question, click Hint 3 times. Verify hints escalate from nudge to strategy to first step, and counter decreases.
- [ ] **Wrong answers reset streak.** Answer incorrectly. Verify streak resets to 0 and difficulty may decrease after 2 wrong.
- [ ] **Complete a practice session (~10 questions).** Verify summary appears with correct/total count and accuracy percentage.
- [ ] **Resume an active practice session.** Start a practice session, navigate away, then come back. Verify the resume banner appears and clicking it restores the session.
- [ ] **Practice history.** After completing a session, go to the practice picker. Verify the completed session shows in the history section.
- [ ] **End practice early.** Start a session, answer a few questions, then click End Practice. Verify stats summary appears and you return to the picker.

### Priority 3 — Diagnostic → Lesson Pipeline

- [ ] **Complete a diagnostic for a second subject (e.g., Science).** Go through the full diagnostic. Verify a Science Lesson card appears on the home screen.
- [ ] **Lesson recommendations match weakest areas.** After completing a Science diagnostic, check that the recommended topic is the one with the lowest score.
- [ ] **Retake a diagnostic.** Use the Restart button on a completed diagnostic. Verify the profile updates and lesson recommendations change accordingly.

### Priority 4 — Edge Cases & Navigation

- [ ] **Resume a lesson after page refresh.** Start a lesson, send a couple messages, then refresh the browser (F5). Click the resume banner. Verify all messages restore correctly.
- [ ] **Switch between lesson and tutor mode for the same subject.** Start a Math lesson, then open tutor mode. Verify no lesson progress bars. Go back to lessons and resume — verify state is intact.
- [ ] **Rapid mode switching.** Quickly click between Home, Diagnostic Results, Lessons, and a subject. Verify no panels overlap or progress bars appear in wrong modes.
- [ ] **Long lesson conversation.** Go through 15+ messages in a single lesson. Verify scrolling works and messages don't overlap.
- [ ] **Empty input.** Try clicking Send with an empty input field in all three modes. Nothing should happen.

### Priority 5 — Visual / UX

- [ ] **Score badge colors.** On the lesson picker, verify: Advanced = blue, Proficient = green, Developing = orange/yellow, Needs Work = red.
- [ ] **Mobile / narrow window.** Resize the browser window narrow. Note any layout issues with the sidebar, topic grid, or chat area.
- [ ] **Typing indicator timing.** During any API call, verify the Thinking... indicator appears while waiting and disappears when the response arrives.

### Priority 6 — Student Accounts & Personalization

- [ ] **Data isolation.** Log in as Student A, start a Math tutor conversation, log out. Log in as Student B and open Math tutor — verify the conversation is empty (not Student A's).
- [ ] **Badge earning.** As a new student, complete a diagnostic. Verify the "First Steps" badge toast appears. Check My Profile to confirm the badge is displayed.
- [ ] **Personalized tutor responses.** Start a tutor chat and a lesson. Verify Claude addresses the student by name at least once in each mode.
- [ ] **Edit Profile.** Click My Profile → Edit Profile. Change the student's name and avatar. Log out and back in — verify the changes persisted.
- [ ] **Wrong PIN rejection.** Select a student and enter an incorrect 4-digit PIN. Verify the error message appears and you are not logged in.
- [ ] **Multiple students on home screen.** Create 3+ student accounts. Verify all cards appear on the login screen with correct names, avatars, and grades.
- [ ] **Legacy data migration.** If flat data exists in data/sessions, use the migrate endpoint. Log in as the target student and verify diagnostic results and sessions are present.
- [ ] **Logout clears state.** Log in, navigate to a lesson, then click Logout. Log back in as a different student — verify no leftover state from the previous student.

### Priority 7 — Parent Dashboard

- [ ] **Navigate to /parent.** Verify the PIN login screen renders with a numeric keypad.
- [ ] **Enter default PIN 0000.** Verify the dashboard loads with student selector dropdown.
- [ ] **Overview panel shows correct counts.** Session, lesson, mastery, and days active counts for the selected student.
- [ ] **Radar chart renders.** Subject scores displayed with hover tooltips.
- [ ] **Skill gap table.** Weakest topics first with color-coded level badges.
- [ ] **Session history filters.** Filter by subject and by type (lesson/practice).
- [ ] **Progress section.** Bar chart and earned badges with dates.
- [ ] **Switch students.** Use the dropdown to select a different student. Verify all sections update.
- [ ] **Change parent PIN.** Via /api/parent/setup. Verify old PIN no longer works.
- [ ] **Responsive layout.** Resize browser to tablet/mobile width. Verify layout adapts.

### Priority 8 — Multi-Tenancy & Customization

- [ ] **Create a new instance.** Use the admin API to create a new family instance. Verify the instance appears in the registry and has its own data directory.
- [ ] **Instance isolation.** Create a student in Instance A and Instance B. Verify they cannot see each other's data.
- [ ] **Custom subject creation.** In the parent dashboard Customization tab, create a custom subject (e.g., "Music Theory") with topics. Verify it appears in the student UI.
- [ ] **Subject toggles.** Disable a master subject (e.g., Latin) from the Customization tab. Verify it no longer appears in the student subject list.
- [ ] **Branding.** Set a custom app title and accent color. Verify both student and parent UIs reflect the changes.
- [ ] **Feature flags.** Disable diagnostics via feature flags. Verify the diagnostic option is hidden from the student.

### Priority 9 — Diagnostics & Feedback

- [ ] **Schedule a diagnostic.** From the parent Diagnostics tab, schedule a Math diagnostic. Log in as the student and verify the pending banner appears.
- [ ] **Start pending diagnostic.** Click "Start Now" on the pending diagnostic banner. Verify the diagnostic launches.
- [ ] **Delete diagnostic results.** From the parent Diagnostics tab, delete a completed diagnostic. Verify the data is removed and the subject shows "Not Started."
- [ ] **Student submits feedback.** Click the feedback button on the student welcome screen. Submit a feature request. Verify it appears as "pending" in the parent Feedback tab.
- [ ] **Parent approves feedback.** Approve the student's feedback from the Feedback tab. Verify the status changes to "approved."
- [ ] **Promote feedback to platform.** Promote approved feedback. Verify it appears in the admin dashboard at /admin.
- [ ] **Admin dashboard.** Navigate to /admin. Verify instance count, feedback stats, and platform feedback list are correct.

---

## Bugs Found & Fixed During Testing

| Bug | File | Root Cause | Fix |
|-----|------|-----------|-----|
| Student feedback modal fails silently | index.html | Code referenced `currentStudent.student_id` but the variable is `currentStudentId` (no student object exists) | Changed to `currentStudentId` in `submitStudentFeedback()` |
| Pending diagnostic check fails silently | index.html | Same `currentStudent` reference in `checkPendingDiagnostics()` | Changed to `currentStudentId` |
| Pending diagnostic banner doesn't auto-show on login | index.html | `checkPendingDiagnostics()` was hooked to nonexistent `showWelcomeScreen` function | Added `setTimeout(checkPendingDiagnostics, 500)` to `loginSuccess()` |
| All 12 POST endpoints crash when `instance_id` not in request body | app.py | `instance_id = request.instance_id or instance_id` causes `UnboundLocalError` — Python treats the left-side assignment as creating a local variable, making the right-side reference undefined | Changed all 12 occurrences to `instance_id = request.instance_id or "default"` |
| Diagnostics tab empty on non-default instances | app.py + data | `diagnostics_pending.json` initialized as `[]` instead of `{}`, causing `AttributeError` when code calls `.get()` on a list | Fixed data files to `{}`; added `isinstance(data, dict)` guard in `load_diagnostics_pending()` |
| Diagnostic progress lost when leaving mid-assessment | index.html + app.py | No resume infrastructure for diagnostics (unlike lessons which had full resume lifecycle) | Added `/api/diagnostic/active/{subject}` endpoint, resume badge on diagnostic grid, active session check before starting fresh |
| Switching students on Diagnostics tab doesn't reload data | parent.html | `renderDashboard()` (called by `switchStudent()`) didn't reload tab-specific data like diagnostics or feedback | Added active tab detection to `renderDashboard()` — auto-calls `loadDiagnostics()` or `loadFeedback()` if those tabs are visible |
| Generic "Couldn't connect" error hides real errors | index.html | All 9 catch blocks showed the same generic message with no error detail | Added `console.error("API error:", err)` and appended `err.message` to displayed UI message |
| Parent dashboard Overview shows zero for non-default instances | app.py | Five aggregate functions didn't accept `instance_id` — always read from default instance data | Added `instance_id` parameter to all 5 aggregate functions; instance dashboard endpoint passes it throughout |
| Diagnostics not counted in Overview stats or Session History | app.py + parent.html | `aggregate_student_overview` only counted lessons/practice; `build_session_history` excluded diagnostics | Added diagnostic counting to total_sessions and session history; added "Diagnostics" filter option |
| Diagnostic sessions don't register as activity days | app.py | `diagnostic_start` didn't update student `activity_dates` | Added activity_dates tracking to `diagnostic_start` endpoint |
| All 8 Claude API calls crash silently on error | app.py | No try-except around `client.messages.create()` — any API failure (auth, rate limit, network) causes unhandled 500 error | Created `call_claude()` helper with error handling; replaced all 8 raw API calls; returns 502 with actual error message |
| Frontend silently fails on API errors | index.html | `await res.json()` called without checking `res.ok` — non-JSON 500 error pages crash JSON parsing silently | Created `safeFetchJSON()` helper; updated all 8 critical POST fetch calls to check response status and extract error detail |
| Greeting elements destroyed on logout causes crash for next student | index.html | `logout()` set `messages.innerHTML = ""` which destroyed the greeting div; next student's `selectSubject` crashed with `TypeError: Cannot set properties of null` when accessing `greetingIcon` | Changed logout to preserve greeting structure; added null guards on all greeting element accesses |
| Stale diagnostic progress bar shown after student switch | index.html | Progress bar, cached `diagnosticResults`, and lesson/practice IDs not cleared on logout | Added `updateDiagProgress(0)`, `diagnosticResults = {}`, and ID resets to `logout()` |
| LaTeX rendering shows HTML entities in math expressions | index.html | HTML escaping ran BEFORE LaTeX extraction in `renderFormattedContent()`, so KaTeX received `&lt;` instead of `<` | Reordered: extract LaTeX expressions first, THEN escape HTML on remaining text |
| Diagnostic input bar locked after completing an assessment | index.html | `messageInput.disabled = true` set on diagnostic completion was never reset when starting a new diagnostic for another subject | Added `messageInput.disabled = false` and `sendBtn.disabled = false` in `selectSubject` for diagnostic mode |
| New student not appearing in parent dashboard dropdown | parent.html | `addStudent()` called `loadSettings()` to refresh PIN table but did not refresh the student selector dropdown | Added `loadStudents()` call after successful student creation |
| Subject enable/disable and custom subjects ignored for students | app.py | `/api/subjects` endpoint iterated over hardcoded `SUBJECTS` dict, ignoring `enabled_subjects` and `custom_subjects` from instance config | Changed to use `get_enabled_subjects(instance_id)` which respects toggle state and includes custom subjects |
| Practice mode crashes with 500 (save_practice_log) | app.py | `save_practice_log()` missing `instance_id` parameter that all 3 call sites were passing — `TypeError: unexpected keyword argument` | Added `instance_id` param to function signature and passed it through to `practice_dir_for_subject()` |
| All 19 API endpoints reject custom subjects | app.py | Every endpoint checked `subject not in SUBJECTS` against the hardcoded master dict; custom subjects always returned "Unknown subject" | Created `resolve_subject(key, instance_id)` helper; replaced all 19 checks and 6 `SUBJECTS[subject]` lookups in system prompt builders |
| Diagnostic prompt crashes for subjects with < 6 topics | app.py | `build_diagnostic_system_prompt()` hardcoded `topics[0]` through `topics[5]` in the example JSON — `IndexError` for custom subjects with fewer topics | Dynamic topic list generation using list comprehension over actual topics |
| Practice difficulty increases after wrong answer | app.py | `adjust_difficulty()` called before answer evaluation — saw prior streak of 3 and bumped up, then streak was reset to 0 afterward | Moved difficulty adjustment to after correctness is determined |
| Practice counts unanswered question in score | app.py | `question_count` incremented when Claude posed a new question, even if student ended practice before answering | Added `answered_count` tracking; stats and accuracy now use answered questions only |

### Known Minor Issues

- **"null%" on Diagnostics tab** — Math diagnostic card on the parent Diagnostics tab shows "null%" instead of the actual score percentage. Functional but cosmetic. The data is correct in the backend; the display template doesn't handle the score format properly.

---

## E2E Test Plan

A comprehensive end-to-end test plan was created to verify all built features before proceeding to the guide and intake form. The plan uses a dedicated clean test instance with no prior data.

### Test Instance

| Property | Value |
|----------|-------|
| Instance ID | `aea9b4fb3810` |
| Instance Name | E2E Test Tutor |
| Parent PIN | `9999` |
| Student A | Alex — PIN `1234`, avatar 🦊, Grade 8 |
| Student B | Jordan — PIN `5678`, avatar 🚀, Grade 7 |
| Student URL | `/f/aea9b4fb3810` |
| Parent URL | `/f/aea9b4fb3810/parent` |

### Test Coverage (74 Tests, 12 Sections)

| Section | Tests | What's Verified |
|---------|-------|-----------------|
| 1. Instance Access & Routing | 5 | URL routing, tunnel access, invalid IDs, admin dashboard |
| 2. Authentication & Student Accounts | 8 | PIN login (wrong/right), parent login, data isolation, student switching |
| 3. Diagnostic Assessment | 8 | Start, interrupt/resume, complete, multi-subject, safety filter |
| 4. Lessons | 6 | Topic picker, 5-step structure, interrupt/resume, new lesson reset |
| 5. Practice / Drills | 5 | Adaptive difficulty, streaks, hints, session summary, tunnel access |
| 6. Math Rendering (Feature 20) | 4 | Fractions, exponents, radicals, markdown formatting, non-STEM check |
| 7. Parent Dashboard | 12 | Overview stats, activity calendar, subject breakdown, session history, diagnostics tab, student switching, customization, feedback, settings, add student |
| 8. Feedback System | 4 | Student feedback submission, parent view, promotion, admin dashboard |
| 9. Customization & Settings | 5 | PIN change, subject enable/disable, custom subjects |
| 10. Badges & Gamification | 3 | First diagnostic badge, badge timeline, all-subjects badge |
| 11. Edge Cases & Safety | 5 | Off-topic redirect, rapid-fire, dual tabs, long input, page refresh |
| 12. Round 2 — Regression Retests | 9 | Diagnostic input bar fix, LaTeX rendering, student dropdown refresh, subject toggle, custom subject diagnostics |

### E2E Test Results

**Round 1:** 52/65 passed (80%) — 6 failures identified and fixed, 2 skipped.

**Round 2:** All 6 previously-failed tests confirmed fixed. Practice mode validated (5.1–5.3, 5.5 pass). All 9 regression tests (12.1–12.9) passed. Two practice scoring bugs found and fixed (difficulty adjustment timing, unanswered question counting).

**Status:** All features passing. Only remaining untested item is completing all 5 subject diagnostics for the "All Subjects" badge (test 10.3) — functional but time-intensive (~90 questions).

### Test Plan UI Features

The test plan is an interactive HTML file (`e2e_test_plan.html`) with pass/fail/skip buttons per test, section-level notes fields, a sticky progress bar with pass/fail breakdown, localStorage persistence, and a one-click "Export Results as Text" feature for clipboard copy.

---

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1–3) — "He Can Talk to the Tutor"

| Feature | Deliverable | Status |
|---------|------------|--------|
| Feature 1 | Working chat interface with Claude as tutor | COMPLETE |
| Feature 2 | Diagnostic assessments for all 5 subjects | COMPLETE |
| Feature 3 | Personalized 5-step lessons from diagnostics | COMPLETE |

### Phase 2: Learning (Weeks 3–6) — "The Tutor Teaches, Practices, and Tracks"

| Feature | Deliverable | Status |
|---------|------------|--------|
| Feature 4 | Practice engine with exercises, hints, streaks, difficulty scaling | COMPLETE |
| Feature 5 | Student accounts, multi-user support, badges, data isolation | COMPLETE |
| Feature 5.5 | Content safety guardrails: age-appropriate content, input filtering, injection protection | COMPLETE |

### Phase 3: Visibility (Weeks 6–7) — "You Can See Progress"

| Feature | Deliverable | Status |
|---------|------------|--------|
| Feature 6 | Parent dashboard with charts, stats, and activity history | COMPLETE |

### Phase 4: Monetization & Family Features (Weeks 7–8) — "Ready for Multiple Families"

| Feature | Deliverable | Status |
|---------|------------|--------|
| Feature 7 | Multi-tenancy with instance-per-family isolation | COMPLETE |
| Feature 8 | Platform customization — subjects, branding, feature flags | COMPLETE |
| Feature 9 | Ad hoc diagnostics & parent controls | COMPLETE |
| Feature 10 | Feedback mechanism with approval workflow and admin dashboard | COMPLETE |
| Feature 11 | Parent PIN management — Settings tab with PIN reset | COMPLETE |
| Feature 12 | Path-based instance URL routing — `/f/{id}` and `/f/{id}/parent` | COMPLETE |

### Phase 5: Demo-Ready (Weeks 9–10) — "Ready to Show the World"

| Feature | Deliverable | Status |
|---------|------------|--------|
| Feature 23 | Product tour, feature guidance, and help section with training guide | **Complete** |
| Feature 20 | Visual math rendering with KaTeX | **Complete** |
| Feature 17 | Gamification system with XP, 10 levels, daily streaks, level-up animations, XP toasts | Complete |

### Phase 6: Onboarding (Weeks 10–12) — "New Families Can Self-Serve"

| Feature | Deliverable | Status |
|---------|------------|--------|
| Feature 13 | Family invite links — shareable URLs that auto-create instances | **Complete** |
| Feature 24 | Onboarding intake form — guided setup that configures the tutor to each family | **Complete** |

### Phase 7: Intelligence (Weeks 12–16) — "The Tutor Gets Smarter"

| Feature | Deliverable | Status |
|---------|------------|--------|
| Feature 14 | Adaptive learning engine with spaced repetition | ✅ Complete |
| Feature 15 | Periodic reassessments with growth tracking — auto-scheduled checkpoints, parent controls, growth charts | ✅ Complete |
| Feature 16 | Schoolwork upload — tutor analyzes, generates practice, tracks grades | ✅ Complete |

### Phase 8: Engagement Modes (Weeks 16–20) — "The Tutor Becomes Irresistible"

| Feature | Deliverable | Status |
|---------|------------|--------|
| Feature 18 | Socratic mode with guided questioning | **Complete** |
| Feature 21 | Quick quiz and flashcard study mode | **Complete** |
| Feature 22 | Study timer with session goals and Pomodoro | ✅ Complete |
| Feature 19 | Voice input and text-to-speech accessibility (STT + TTS with Zoe Premium) | ✅ Complete |

### Phase 9: Growth & Accessibility (Weeks 20–24) — "The Tutor Grows With the Student"

| Feature | Deliverable | Status |
|---------|------------|--------|
| Feature 25 | Grade scaling (6–12) — dynamic prompts, topics, and safety rules by grade | ✅ Complete |
| Feature 26 | ADD/ADHD adaptability — chunking, pacing, refocus, session presets, reduced cognitive load | Planned |
| Feature 27 | Parent safety transparency — safety log UI, conversation viewer, safety summary | ✅ Complete |

### Phase 10: Monetization & Growth (Weeks 24–28) — "The Platform Pays for Itself"

| Feature | Deliverable | Status |
|---------|------------|--------|
| Feature 30 | Family referral program — unique codes, two-sided rewards, tiered incentives, Stripe credits | Planned |
| Feature 34 | Book review mode — chapter-by-chapter reading comprehension, grade-adaptive discussion, book library | ✅ Complete |

### Phase 15: AI Accessibility & User Proficiency — "Meet Them Where They Are"

| Feature | Deliverable | Status |
|---------|------------|--------|
| Feature 57 | Guided conversation mode — prompt chips, follow-up suggestions, confusion button, automatic progression, guided vs. open mode | ✅ Complete |
| Feature 58 | Adaptive response complexity — 4-tier calibration system, diagnostic-driven, in-session adaptation, grade/goal/proficiency-weighted | ✅ Complete |
| Feature 59 | AI proficiency & onboarding enhancements — familiarity question in setup, smart defaults, Getting Started card, contextual tooltips, student mini-tutorial | ✅ Complete |
| Feature 60 | Expedition activity templates — 8 named conversation templates (Word Explorer, Evidence Trail, Dialogue Workshop, Expedition Challenge, Skill Drill, Lab Log, Chronicle Map, Compass Review) with subject-specific flows, stage-based prompt chips, anxiety-reducer framing | Planned |

### Phase 14: Atlas Brand Adoption — "The Tutor Has an Identity"

| Feature | Deliverable | Status |
|---------|------------|--------|
| Feature 51 | Visual theme — atlas-theme.css design tokens, color palette, typography | ✅ Complete |
| Feature 52 | AI voice system — two-tier (middle/high school) voice in atlas_voice.py | ✅ Complete |
| Feature 53 | UX language — exploration metaphors on student surfaces, hybrid approach | ✅ Complete |
| Feature 54 | Parent portal visual refresh — apply Atlas colors/fonts to parent.html | ✅ Complete |
| Feature 55 | Help content & glossary update — Atlas terminology in guide.html, parent FAQ, student help | ✅ Complete |
| Feature 56 | Background watermarks — globe, compass rose, topo lines, grid | ✅ Complete |

---

## Feature 29: Admin Dashboard
**Critical | Status: ✅ Complete (29A-G)**

The current admin page (`/admin`) is a placeholder with no interactive functionality. This feature builds it into a full operational dashboard for managing the platform — responding to families, troubleshooting issues, and monitoring usage.

### 29A: Instance Management
**Priority: Highest**

View and manage all family instances from one place.

- [ ] Instance list view — family name, created date, student count, last active, status
- [ ] Click into any instance to view full config, students, and activity summary
- [ ] Reset parent PIN from admin (for lockout situations)
- [ ] Reset student PIN from admin
- [ ] Deactivate/reactivate an instance
- [ ] Search and filter instances by name, date, or status

### 29B: Feedback Management
**Priority: Highest**

Centralized feed for all student and parent feedback with the ability to respond.

- [ ] Unified feedback inbox — all feedback across all instances in one view
- [ ] Reply to feedback with a message back to the family
- [ ] Mark feedback as resolved, acknowledged, or needs follow-up
- [ ] Filter by instance, feedback type (bug/feature/content/general), or status
- [ ] Feedback notification count (unread/unresolved)

### 29C: Student Oversight
**Priority: High | Status: Complete**

Ability to see what any student is seeing and review their progress.

- [x] Read-only view into any student's current state (mastery, diagnostics, growth)
- [x] View conversation logs for any student session
- [x] View diagnostic results and growth history per student
- [x] Quick-link to jump into a student's portal view

### 29D: Safety & Moderation
**Priority: High**

Cross-instance safety monitoring and incident management.

- [x] View safety logs across all instances (flagged conversations)
- [x] Review full conversation context when something is flagged
- [x] Add admin notes to a safety incident
- [x] Filter by severity, instance, or date

### 29E: Invite Management
**Priority: Medium**

Manage invite codes without needing API calls.

- [x] View all active invite codes — creator, usage count, expiration, status
- [x] Create new invite codes directly from admin UI
- [x] Revoke invites with one click
- [x] View which instances were created from each invite

### 29F: Usage Analytics
**Priority: Medium**

High-level platform metrics to understand engagement.

- [x] Dashboard cards — total instances, active students, sessions this week, lessons completed
- [x] Subject popularity breakdown
- [x] Engagement tracking — students who haven't logged in recently
- [x] Activity trends over time (daily/weekly)

### 29G: System Health
**Priority: Lower**

Operational visibility into the platform.

- [x] Claude API call tracking (usage/cost awareness)
- [x] Error log viewer (recent server errors)
- [x] Server uptime and status indicator

---

## Feature 30: Family Referral Program
**Important | Status: Planned**

### What It Does
A family-to-family referral system that rewards existing users for bringing new families to the platform. Each family receives a unique referral code they can share. Both the referring family and the new family receive benefits — creating a two-sided incentive that drives organic growth while keeping acquisition costs near zero.

### Key Components

- **Unique referral codes** — Each family automatically receives a referral code tied to their instance ID (e.g., `REF-{short_hash}`). Codes are generated at instance creation and displayed in the parent Settings tab. Families can copy the code or share a referral link (`/signup?ref={code}`) directly.
- **Two-sided reward structure** — Both the referrer and the referred family benefit. The referrer's reward depends on what tier the new family signs up for. The referred family (invitee) always receives a first-month discount as a welcome incentive.
- **Tiered referrer rewards** — Rewards scale with the value of the new signup:
  - **Referred family joins Free tier:** Referrer gets a 10–15% discount on their next billing cycle
  - **Referred family joins Family ($19/mo) or Academy ($29/mo) tier:** Referrer gets a full free month
- **Invitee benefit** — The referred family receives their first month at a discounted rate (e.g., 25–50% off) when signing up through a referral link. This applies to Family and Academy tiers only (Free tier is already free).
- **Annual cap** — Referrers can earn a maximum of 3 free months per calendar year from referrals. This prevents abuse while still rewarding active advocates. Percentage discounts (from Free-tier referrals) do not count toward the cap. The cap resets January 1.
- **Referral tracking** — Every referral event is logged with: referrer instance ID, referred instance ID, referral code used, date referred, tier the new family selected, reward type issued, and redemption status (pending/applied/expired).
- **Reward lifecycle** — When a referred family signs up and remains active past a qualifying period (e.g., 14 days or first billing cycle), the referrer's reward is marked as "earned" and applied to their next billing cycle. If the referred family cancels or downgrades to Free before the qualifying period, the reward is voided.
- **Parent Settings UI** — A "Referrals" section in the parent Settings tab showing: the family's referral code with a copy button, a shareable referral link, a count of successful referrals, earned rewards and their status (pending/applied/expired), and remaining free months available this year.

### Technical Details

**Phase 1 — JSON stage (≤100 families):**
- New file: `data/referrals.jsonl` — append-only ledger with one JSON object per referral event: `{ referrer_id, referred_id, code, tier, reward_type, reward_status, created_at, qualified_at, applied_at }`
- New file per instance: `data/instances/{id}/referral_code.json` — stores the family's unique code and reward balance
- New endpoints:
  - `GET /api/instance/{id}/referral` — returns the family's referral code, stats, and reward history
  - `POST /api/referral/redeem` — called during onboarding when a new family signs up with a referral code; validates the code, links the referral, and marks the invitee discount
  - `GET /api/referral/validate/{code}` — public endpoint for the signup page to verify a referral code is valid
- Reward application is manual at the JSON stage — admin reviews and applies credits via the admin dashboard
- Referral code generation: `REF-` + first 8 chars of a SHA-256 hash of the instance ID + creation timestamp

**Phase 2 — PostgreSQL stage (1,000+ families):**
- New table: `referrals` with columns: `id`, `referrer_instance_id`, `referred_instance_id`, `referral_code`, `referred_tier`, `reward_type` (enum: percentage_discount, free_month), `reward_status` (enum: pending, qualified, applied, expired, voided), `invitee_discount_applied` (boolean), `created_at`, `qualified_at`, `applied_at`
- New table: `referral_codes` with columns: `instance_id`, `code` (unique index), `total_referrals`, `free_months_used_this_year`, `year`
- Stripe integration: rewards are applied as billing credits (for free months) or coupon codes (for percentage discounts) via the Stripe API. When a reward qualifies, a webhook handler creates a Stripe credit note or applies a coupon to the referrer's next invoice automatically.
- Invitee discounts are applied as Stripe coupons attached to the subscription at creation time when a valid referral code is present.
- Annual cap enforcement: query `referrals` table for `reward_type = 'free_month' AND reward_status = 'applied' AND year = current_year` grouped by `referrer_instance_id`; reject new free-month rewards when count ≥ 3.

### Acceptance Criteria

- [ ] Every family instance has a unique, persistent referral code
- [ ] Referral code is displayed in parent Settings with copy-to-clipboard functionality
- [ ] Signing up with a valid referral code links the new family to the referrer
- [ ] Referrer receives correct reward based on the referred family's tier selection
- [ ] Referred family receives first-month discount when using a referral code
- [ ] Rewards are voided if the referred family cancels before the qualifying period
- [ ] Referrers cannot earn more than 3 free months per calendar year
- [ ] Referral history is visible in parent Settings (who they referred, reward status)
- [ ] Invalid or expired referral codes show a clear error during signup
- [ ] At PostgreSQL stage: Stripe credits/coupons are applied automatically at billing time

### Estimated Scope
- JSON stage: ~100 lines in app.py (endpoints, referral logic), ~80 lines in parent.html (Settings UI), ~30 lines in onboarding flow (referral code input)
- PostgreSQL stage: ~150 lines for migration and Stripe webhook integration

---

## Feature 34: Book Mastery Mode
**Important | Status: ✅ Complete**

**Deployed in v1.3.0 (March 26, 2026)**

### What It Does
A dedicated reading comprehension mode where students work through books chapter by chapter with the AI tutor. The tutor guides discussion, checks understanding, asks probing questions, and builds critical thinking skills — functioning like a one-on-one book club with an infinitely patient literary coach. Available on Family and Academy tiers only, making it a key conversion driver from Free to paid.

### Key Components

- **Student-initiated book selection (primary flow)** — The student tells the tutor what book they're currently reading. The tutor uses Claude's knowledge to identify the book, confirm the title and author, and set up a chapter-by-chapter review structure. This is the expected main use case — students bring their own school assignments, independent reading, or personal interest books.
- **Tutor-suggested books (secondary flow)** — The tutor can recommend books based on the student's grade level, subject interests, and reading history. Suggestions are calibrated by grade: middle school students (6–8) receive age-appropriate titles; high school students (9–12) receive progressively more challenging works. The student picks from the suggestion list and the review begins.
- **Chapter-by-chapter review structure** — Each book is tracked as a series of chapter reviews. When a student starts a new chapter review, the tutor asks what happened in the chapter, then guides a structured discussion covering: plot comprehension (what happened), character analysis (motivations, development, relationships), theme identification (recurring ideas, symbolism), vocabulary in context (challenging words encountered), and personal response (opinions, connections to other reading or personal experience).
- **Adaptive questioning by grade** — The tutor calibrates depth and vocabulary to the student's grade level. For grades 6–8: focus on plot recall, character traits, basic theme identification, and vocabulary building. For grades 9–12: deeper analysis of narrative technique, authorial intent, historical context, unreliable narration, allegory, and argumentative writing about themes.
- **Reading progress tracker** — A visual progress view showing: the book title and author, chapters completed vs. total (if known), comprehension scores per chapter, and overall book progress. Displayed on the student welcome screen when a book is active, and summarized in the parent dashboard.
- **Comprehension scoring** — Each chapter review produces a comprehension score based on the quality and completeness of the student's responses across the five discussion areas (plot, character, theme, vocabulary, personal response). Scores feed into the parent dashboard and the adaptive learning engine for ELA skill tracking.
- **Book library** — A per-student log of all books reviewed, with completion status, chapter scores, and date ranges. Accessible from a "My Books" section in the student sidebar. Completed books show an overall comprehension score and a brief AI-generated summary of the student's growth across the book.
- **Tier gating** — Book Review is locked behind the Family ($19/mo) and Academy ($29/mo) tiers. Free-tier students see the Book Review option in the sidebar but receive a prompt to upgrade. The feature name and description are visible on the Free tier to drive conversion interest.
- **XP integration** — Completing a chapter review awards XP (e.g., 35 XP per chapter, 100 XP bonus for finishing a book). Book-related badges are added to the gamification system (e.g., "First Chapter", "Bookworm — 5 books completed", "Literary Scholar — 10 books").

### Technical Details

- **New data structure per student:** `data/instances/{id}/students/{sid}/books/` directory containing one JSON file per book: `{ book_id, title, author, total_chapters, chapters_reviewed: [{ chapter_number, date, comprehension_score, discussion_log }], status: active|completed|abandoned, started_at, completed_at }`
- **New endpoints:**
  - `POST /api/book/start` — Initialize a new book review. Accepts title (required), author (optional — Claude identifies if omitted), total_chapters (optional). Returns book_id and confirmation.
  - `POST /api/book/suggest` — Returns a list of 5–8 grade-appropriate book suggestions based on student grade, subject interests, and books already read. Claude generates suggestions with brief descriptions.
  - `POST /api/book/chapter/start` — Begin a chapter review session. Accepts book_id and chapter_number. Returns the opening discussion prompt from the tutor.
  - `POST /api/book/chapter/message` — Send a message within a chapter review discussion. Returns the tutor's response with discussion guidance.
  - `POST /api/book/chapter/complete` — End a chapter review. Claude scores comprehension across the five areas and returns a summary. Awards XP.
  - `GET /api/book/library/{student_id}` — Returns the student's book library (all books, statuses, scores).
  - `GET /api/book/active/{student_id}` — Returns the currently active book and chapter progress.
- **System prompt:** A `BOOK_REVIEW_PROMPT` constant in app.py containing discussion structure rules, grade-calibrated questioning guidelines, and instructions for scoring. Appended to the base system prompt during book review sessions. Includes the Atlas voice overlay when Atlas brand is active.
- **Tier enforcement:** Endpoints check the instance's subscription tier before allowing access. Free-tier requests return a 403 with an upgrade message.
- **Parent dashboard integration:** A new "Reading" card on the parent Overview tab showing: active book title, chapters completed, average comprehension score. Full book history available in a "Reading" sub-tab or section within the existing Overview.
- **Sidebar navigation:** New "📚 Books" button in the student sidebar, positioned after Study mode. Opens the book library view with options to continue an active book, start a new book, or browse suggestions.

### Acceptance Criteria

- [ ] Student can start a book review by telling the tutor what they're reading
- [ ] Tutor correctly identifies the book and sets up chapter tracking
- [ ] Tutor can suggest grade-appropriate books when asked
- [ ] Chapter reviews cover all five discussion areas (plot, character, theme, vocabulary, personal response)
- [ ] Discussion depth adapts to the student's grade level (6–8 vs. 9–12)
- [ ] Each chapter review produces a comprehension score
- [ ] Book progress is tracked and visible on the student welcome screen
- [ ] Book library shows all reviewed books with scores and completion status
- [ ] Completing chapters and books awards XP and triggers badge checks
- [ ] Book Review is locked on Free tier with an upgrade prompt
- [ ] Parent dashboard shows reading activity and comprehension scores
- [ ] Student can resume an interrupted chapter review

### Estimated Scope
- ~200 lines in app.py (endpoints, book review prompt, comprehension scoring, tier gating)
- ~250 lines in index.html (book library UI, chapter review interface, sidebar nav, progress tracker)
- ~80 lines in parent.html (reading card on Overview, book history section)
- ~30 lines for XP and badge integration in existing gamification code

---

## Feature 57: Guided Conversation Mode
**Critical | Status: ✅ Complete**

**Deployed in v1.3.0 (March 26, 2026)**

### Origin
User testing feedback (March 2026): Parents reported that students — especially those unfamiliar with AI chat — don't know what questions to ask, leading to unproductive sessions. A tester noted: "I'm not sure students will ask the right questions to get what they need." As the designer, the instinct is to dig deeper and reprompt when AI output isn't quite right, but we can't assume that proficiency in our users. Atlas must actively guide the conversation rather than waiting passively for student input.

### What It Does
A conversation scaffolding system that ensures students always have a clear next step — whether they're AI-savvy or have never chatted with an AI before. Instead of presenting a blank text box and hoping the student knows what to type, Atlas proactively offers conversation starters, contextual follow-up suggestions, and automatic progression through learning objectives. The intensity of guidance adapts based on the family's self-reported AI proficiency (captured during onboarding — see Feature 59) and the student's in-session behavior.

### Key Components

- **Territory entry prompts** — When a student enters a subject (territory), Atlas doesn't wait for input. It opens with a warm, specific greeting and 2–3 tappable prompt chips: "Pick up where we left off," "I need help with [recent weak topic]," "Explore something new." These are contextual — informed by the student's diagnostic results, recent session history, and current proficiency gaps.
- **Contextual follow-up chips** — After every Atlas response, 2–3 suggested follow-up actions appear as tappable buttons below the message. Examples: "Explain that differently," "Give me a practice problem," "I understand — what's next?" "Can you give me an example?" These are dynamically generated by Claude based on the conversation context, not hardcoded.
- **"I'm confused" button** — A persistent, always-visible button (distinct from the follow-up chips) that the student can tap at any point without needing to articulate what they don't understand. Atlas re-explains the last concept at a simpler level, using a different approach (analogy, visual description, step-by-step breakdown). Tapping it twice in a row triggers an even simpler explanation and suggests the student try a guided practice problem instead of continuing the discussion.
- **Automatic progression** — When Atlas detects that a student has demonstrated understanding of the current concept (via correct answers, quality of responses, or explicit confirmation), it proactively transitions: "Nice work on that. Ready to move on to [next concept]?" This prevents students from stalling in a completed topic because they don't know what to ask next.
- **Session warm-up for new users** — On a student's first 3 sessions, Atlas includes a brief orientation message: "I'm Atlas, your guide. You can type anything you want to learn about, or tap one of the buttons below to get started. There's no wrong answer here." This only appears for the first few sessions and is skippable.
- **Guided mode vs. open mode** — Two conversation modes controlled by a parent toggle in the dashboard Settings tab:
  - **Guided mode (default for low/medium AI proficiency):** Follow-up chips are always shown, automatic progression is active, and Atlas initiates topic transitions. Conversation feels like a structured tutoring session.
  - **Open mode (default for high AI proficiency):** Follow-up chips are shown but less prominently, Atlas responds more conversationally and lets the student lead. Better for students comfortable with AI chat who want more autonomy.
  - Parents can switch between modes at any time. The mode is stored per-student.

### Technical Details

- **Follow-up chip generation:** Each Claude API response includes an additional instruction in the system prompt to return 2–3 suggested follow-ups in a structured JSON block appended to the response. The front end parses and renders these as tappable chips. Example schema: `{"followups": ["Explain differently", "Practice problem", "What's next?"]}`
- **Confusion handler:** The "I'm confused" button sends a special flag with the next API call (`confused: true, confusion_count: N`). The system prompt instructs Claude to re-explain using a different modality. On `confusion_count >= 2`, the prompt shifts to guided practice mode.
- **Guided vs. open mode:** Stored in the student JSON as `conversation_mode: "guided" | "open"`. The system prompt includes different instructions based on mode. Parent dashboard Settings tab gets a new toggle per student.
- **Session count tracking:** A `session_count` field per student tracks total sessions for the new-user warm-up. After 3 sessions, the orientation message stops.
- **Progression detection:** Claude evaluates whether the student has demonstrated understanding by analyzing their responses. When confidence is high, Claude includes a `progression_ready: true` flag in the response metadata, triggering the "ready to move on" prompt.
- **AI proficiency integration:** The family's `ai_proficiency` setting (see Feature 59) sets the default conversation mode: low → guided, medium → guided, high → open. Parents can override per-student.

### Files Modified
- `app.py` — System prompt additions for follow-up generation, confusion handling, progression detection, conversation mode branching (~80 lines)
- `static/index.html` — Follow-up chip rendering, "I'm confused" button, session warm-up overlay, prompt chip styling and tap handlers (~150 lines)
- `static/parent.html` — Conversation mode toggle in Settings tab per student (~30 lines)
- `static/guide.html` — Training guide section on guided vs. open mode (~20 lines)
- Help content — Update student help, parent FAQ, and parent tour to explain guided conversation features

### Acceptance Criteria

- [ ] Student sees 2–3 tappable prompt chips when entering a territory
- [ ] After every Atlas response, 2–3 contextual follow-up chips appear
- [ ] Follow-up chips are dynamically generated (not hardcoded) and contextually relevant
- [ ] "I'm confused" button is always visible during a conversation
- [ ] Tapping "I'm confused" once re-explains at a simpler level
- [ ] Tapping "I'm confused" twice shifts to guided practice mode
- [ ] Atlas automatically suggests progression when understanding is demonstrated
- [ ] First 3 sessions include a brief orientation message for new students
- [ ] Parent can toggle between Guided and Open mode per student
- [ ] Default mode is set by family AI proficiency level from onboarding
- [ ] All help content (guide, parent FAQ, student help, tour) is updated

### Estimated Scope
- ~80 lines in app.py (system prompt branching, follow-up schema, confusion handler)
- ~150 lines in index.html (chip UI, confusion button, warm-up overlay, mode logic)
- ~30 lines in parent.html (mode toggle in settings)
- ~20 lines in guide.html (training section)
- Help content updates across all surfaces

---

## Feature 58: Adaptive Response Complexity
**Critical | Status: ✅ Complete**

**Deployed in v1.3.0 (March 26, 2026)**

### Origin
User testing feedback (March 2026): A parent noted that Atlas responses are "too wordy and require a high level of critical thinking that my student may not have; hence the need for tutoring." This reveals a fundamental tension — students come to Atlas because they're struggling, but Atlas responds as if they're already proficient. Response complexity must dynamically match the student's ability, not the subject's inherent difficulty.

### What It Does
A response calibration system that adjusts Atlas's vocabulary, sentence structure, explanation depth, and pedagogical approach based on the student's demonstrated ability. This goes beyond simple "make it shorter" — it's a multi-dimensional adaptation that considers grade level, diagnostic results, learning goals (from onboarding), AI familiarity, and real-time session signals. A struggling 7th grader getting help with fractions should receive fundamentally different responses than an advanced 10th grader exploring calculus — even though both are "math."

### Key Components

- **Complexity tiers** — Four response complexity levels, assigned per student per subject:
  - **Foundational (Tier 1):** Short sentences (8–12 words average). Common vocabulary only (no SAT-level words without immediate definition). One concept per response. Heavy use of concrete examples and analogies. Step-by-step breakdowns default to showing every intermediate step. Responses capped at ~100 words before a check-in.
  - **Developing (Tier 2):** Moderate sentence length (12–18 words). Introduces subject-specific vocabulary with in-context definitions on first use. Up to two related concepts per response. Mix of examples and explanation. Responses ~150 words before check-in.
  - **Proficient (Tier 3):** Natural sentence length. Subject vocabulary used freely. Multiple concepts can be connected in a single response. Explanations are more conceptual, less step-by-step. Responses ~200 words.
  - **Advanced (Tier 4):** Full academic register. Abstract reasoning, synthesis across concepts, Socratic questioning. Minimal hand-holding. Responses can be longer and more dense.

- **Tier assignment logic** — A student's tier is determined by a weighted combination of:
  - Diagnostic score for the subject (strongest signal, 50% weight)
  - Grade level (baseline, 20% weight)
  - Learning goals from onboarding — "Catching Up" biases toward Tier 1–2, "Enrichment" toward Tier 3–4 (20% weight)
  - AI proficiency level from onboarding (10% weight — low proficiency nudges down one tier for response density)
  - In the absence of a diagnostic, grade level and learning goals determine the starting tier

- **In-session adaptation** — Atlas adjusts within a session based on real-time signals:
  - Student says "I don't get it," "what?", "huh?", or taps "I'm confused" → Atlas drops one tier for the re-explanation
  - Student gives a strong, detailed response demonstrating understanding → Atlas can nudge up for the next concept
  - Student consistently gives one-word or minimal responses → Atlas stays at current tier but shortens its own responses and asks more yes/no or multiple-choice questions
  - These in-session adjustments don't permanently change the student's tier — they reset next session

- **Permanent tier progression** — A student's base tier for a subject can change over time based on:
  - Diagnostic retakes (new score recalculates tier)
  - Cumulative session performance tracked via a rolling "comprehension confidence" score
  - Tier changes are logged and visible in the parent dashboard

- **Response format adaptation** — Beyond vocabulary and length, the format itself changes by tier:
  - Tier 1–2: More bullet points, numbered steps, and visual breaks. Questions are multiple-choice or yes/no more often. Atlas asks "Does that make sense?" frequently.
  - Tier 3–4: More flowing prose. Open-ended questions. Atlas trusts the student to flag confusion rather than constantly checking.

### Technical Details

- **Tier storage:** Added to the student JSON as `complexity_tiers: { math: 2, science: 1, ela: 3, social_studies: 2 }`. Calculated on diagnostic completion, recalculated on retake. Default (no diagnostic): calculated from grade + learning goals + AI proficiency.
- **System prompt injection:** The `COMPLEXITY_TIER_PROMPT` is a parameterized template inserted into the system prompt before each API call. It includes the tier level, specific vocabulary/length/format constraints for that tier, and the in-session adjustment rules.
- **Tier calculation function:** A new `calculate_complexity_tier(student, subject)` function in app.py that computes the tier from the weighted inputs described above. Called on diagnostic completion and available as a utility for other features.
- **In-session tracking:** The front end tracks confusion signals (button taps, keywords) and sends them as metadata with each API call. The system prompt uses this to adjust response style within the session without permanently altering the tier.
- **Parent dashboard visibility:** The parent Overview tab shows each subject's current tier as a simple label (e.g., "Response Level: Developing"). Parents can see tier progression over time. Parents cannot manually override tiers (to prevent them from setting it too high or too low), but they can request a diagnostic retake to recalculate.

### Files Modified
- `app.py` — `calculate_complexity_tier()` function, `COMPLEXITY_TIER_PROMPT` template, tier recalculation on diagnostic completion, in-session signal processing (~120 lines)
- `static/index.html` — Confusion signal tracking, in-session metadata sending (~40 lines)
- `static/parent.html` — Tier display on Overview tab per subject, tier history (~40 lines)
- `static/guide.html` — Training guide section explaining complexity tiers (~20 lines)
- Help content — Update student help, parent FAQ, and parent tour to explain adaptive responses

### Acceptance Criteria

- [ ] Each student has a complexity tier per subject (default calculated from grade + goals + AI proficiency)
- [ ] Diagnostic completion recalculates the tier for that subject
- [ ] Tier 1 responses are noticeably shorter, simpler, and more scaffolded than Tier 4
- [ ] Atlas vocabulary adjusts by tier (no unexplained SAT words at Tier 1)
- [ ] Response length respects tier-appropriate caps before check-ins
- [ ] In-session confusion signals (button, keywords) cause Atlas to drop a tier temporarily
- [ ] Strong student responses allow Atlas to nudge up within a session
- [ ] Tier is visible to parents on the dashboard per subject
- [ ] Tier changes are logged
- [ ] Students who haven't taken diagnostics get a reasonable default tier
- [ ] All help content (guide, parent FAQ, student help, tour) is updated

### Estimated Scope
- ~120 lines in app.py (tier calculation, prompt template, signal processing)
- ~40 lines in index.html (confusion signal tracking, metadata)
- ~40 lines in parent.html (tier display, history)
- ~20 lines in guide.html (training section)
- Help content updates across all surfaces

---

## Feature 59: AI Proficiency & Onboarding Enhancements
**Important | Status: ✅ Complete**

**Deployed in v1.3.0 (March 26, 2026)**

### Origin
Emerged from the same user testing round as Features 57–58. The designer and primary tester is comfortable with AI and naturally knows how to prompt effectively, but the target audience (parents and students in grades 6–12) may range from "never used AI" to "daily ChatGPT user." A one-size-fits-all onboarding and help experience doesn't serve this range. By capturing AI familiarity early, Atlas can tailor the entire experience — conversation scaffolding, response complexity defaults, help content depth, and parent dashboard guidance.

### What It Does
Adds an AI familiarity question to the onboarding wizard (Step 4: Learning Goals) and uses the response to set intelligent defaults across the platform. Also enhances the post-setup experience for low-proficiency families with a more comprehensive product tour, contextual help tooltips, and a "Getting Started with Atlas" guide in the parent dashboard.

### Key Components

- **Onboarding: AI familiarity question** — Added to Step 4 (Learning Goals) in setup.html. Three options presented as tappable cards (consistent with the existing goal card UI):
  - 🌱 **New to AI** — "We've never used an AI tutor or chatbot before"
  - 🌿 **Somewhat familiar** — "We've tried AI tools a few times"
  - 🌳 **Comfortable** — "We use AI tools regularly"
  - Selection is optional (defaults to "Somewhat familiar" if skipped)
  - Stored in instance config as `ai_proficiency: "low" | "medium" | "high"`

- **Smart defaults from proficiency level:**
  - **Low:** Guided conversation mode (Feature 57) is default for all students. Complexity tiers (Feature 58) start biased one tier lower. Parent tour auto-launches on first dashboard visit. Extended help tooltips are enabled throughout the parent dashboard. A "Getting Started with Atlas" card appears on the parent Overview tab with step-by-step guidance for the first week.
  - **Medium:** Guided conversation mode is default. Standard complexity tier calculation. Tour is offered but not auto-launched. Standard help tooltips.
  - **High:** Open conversation mode is default. Standard complexity tier calculation. Tour is available but not offered. Minimal tooltip intrusion.

- **"Getting Started with Atlas" card (low proficiency)** — A dismissible card on the parent dashboard Overview tab that walks the family through their first week:
  - Day 1: "Have your child log in and complete their first diagnostic assessment"
  - Day 2–3: "Check the dashboard to see diagnostic results and suggested focus areas"
  - Day 4–5: "Your child can start an expedition (lesson) in their weakest territory"
  - Week 1: "Review the weekly summary to see progress"
  - Each step has a checkmark that auto-completes when the action is detected, and a "Learn more" link to the relevant help section
  - Card can be dismissed permanently via an "I've got it" button

- **Enhanced contextual tooltips (low proficiency)** — For low-proficiency families, the parent dashboard shows small ℹ️ tooltip icons next to key elements (subject cards, proficiency bars, diagnostic scores, session history) that expand with plain-language explanations. Example: next to a proficiency bar → "This shows how well your child is doing in this topic. The bar fills up as they practice and improve." These are hidden for medium/high proficiency families unless they enable them in Settings.

- **Student-side onboarding enhancement** — For low-proficiency families, the student's first login includes an interactive mini-tutorial (3–4 screens, skippable):
  - "Atlas is here to help you learn. You can type questions, tap the buttons below messages, or press the 🤔 button if you're ever stuck."
  - "Let's try it! Tap one of these buttons to start your first conversation."
  - "Great! That's all you need to know. Have fun exploring."

### Technical Details

- **Storage:** `ai_proficiency` field added to instance config under `customization`: `"ai_proficiency": "low" | "medium" | "high"`. Default: `"medium"`.
- **Setup wizard change:** New card group in Step 4 of setup.html, after the learning goals grid but before the notes textarea. Submitted with the rest of the setup payload. (~40 lines HTML, ~10 lines JS)
- **Backend:** `POST /api/setup` endpoint updated to accept and store `ai_proficiency`. The `get_instance_config` helper makes it available to all front-end pages.
- **Parent dashboard:** Conditional rendering based on `ai_proficiency`:
  - "Getting Started" card component (~60 lines HTML/JS)
  - Tooltip system: CSS tooltip component + conditional show/hide based on proficiency (~40 lines CSS, ~30 lines JS)
- **Student app:** Mini-tutorial overlay for first login when `ai_proficiency === "low"` (~50 lines HTML/JS)
- **Integration with Features 57 & 58:** The proficiency value is read by the guided mode default logic (Feature 57) and the tier calculation function (Feature 58). These features depend on the `ai_proficiency` field existing.

### Files Modified
- `app.py` — Accept `ai_proficiency` in setup endpoint, include in config response (~15 lines)
- `static/setup.html` — AI familiarity card group in Step 4, JS to capture selection (~50 lines)
- `static/index.html` — First-login mini-tutorial for low proficiency (~50 lines)
- `static/parent.html` — "Getting Started" card, tooltip system, conditional rendering (~130 lines)
- `static/guide.html` — Training guide section on proficiency-based defaults (~20 lines)
- Help content — Update parent FAQ to explain AI proficiency settings and how they affect the experience

### Acceptance Criteria

- [ ] Setup wizard Step 4 includes an AI familiarity question with 3 options
- [ ] Selection is optional and defaults to "medium" if skipped
- [ ] `ai_proficiency` is stored in instance config and accessible to all pages
- [ ] Low-proficiency families get auto-launched parent tour on first visit
- [ ] Low-proficiency dashboard shows "Getting Started with Atlas" card
- [ ] Getting Started card steps auto-complete as actions are detected
- [ ] Getting Started card can be dismissed permanently
- [ ] Low-proficiency dashboard shows contextual tooltips on key elements
- [ ] Low-proficiency students see a mini-tutorial on first login
- [ ] Medium- and high-proficiency families get progressively less hand-holding
- [ ] AI proficiency integrates with Feature 57 (conversation mode default) and Feature 58 (tier bias)
- [ ] All help content (guide, parent FAQ, student help, tour) is updated

### Estimated Scope
- ~15 lines in app.py
- ~50 lines in setup.html
- ~50 lines in index.html
- ~130 lines in parent.html
- ~20 lines in guide.html
- Help content updates across all surfaces

### Build Order Recommendation
Features 59, 57, and 58 should be built in that order, as 57 and 58 both depend on the `ai_proficiency` field created by 59. Feature 60 should be built **after** Feature 57, as it extends the guided conversation infrastructure with activity-specific templates.
1. **Feature 59** — AI Proficiency & Onboarding Enhancements (creates the `ai_proficiency` data field and onboarding UI)
2. **Feature 57** — Guided Conversation Mode (uses `ai_proficiency` to set default conversation mode; builds prompt chip and progression infrastructure)
3. **Feature 58** — Adaptive Response Complexity (uses `ai_proficiency` as a tier calculation input)
4. **Feature 60** — Expedition Activity Templates (uses Feature 57's guided conversation rails to deliver subject-specific activity formats)

---

## Feature 60: Expedition Activity Templates
**Important | Status: Planned**

### Origin
The Iowa Assessments Curriculum Alignment Map (internal reference, March 2026) identified a gap between Atlas's current single-interaction-pattern approach (conversational chat for everything) and the variety of learning experiences students benefit from. The alignment doc proposed named activity types — Word Explorer, Evidence Trails, Lab Logs, Dialogue Workshop, etc. — each with distinct mechanics. Rather than building fully custom UI for each, this feature takes a middle-ground approach: **named conversation templates** that give each activity type a distinct structure and feel while running on the same chat-based infrastructure that Feature 57 establishes.

The key insight: Atlas is a tutor, not a teacher. It doesn't need drag-and-drop widgets or interactive chart manipulation tools. But it does need the conversation to *feel different* depending on what skill is being practiced. A vocabulary session should feel like a word puzzle. A reading comprehension session should feel like a guided passage walkthrough. A computation session should feel like quick-fire drills. The underlying engine is Claude + chat, but the system prompt, conversation scaffolding, pacing, and prompt chip options create a fundamentally different student experience for each activity type.

### What It Does
A library of named activity templates — structured conversation scripts that Atlas follows when a student enters a specific skill area within a territory. Each template defines: an opening format, a conversation flow pattern, the types of prompt chips offered, pacing rules, how responses are structured, and a closing/scoring format. Templates are selected automatically based on the subject, topic, and skill being practiced, or can be offered as choices when a student enters a territory.

### Key Components

**Activity Template Structure**

Each template is a JSON configuration that modifies Atlas's behavior within a conversation. Templates don't replace the chat UI — they shape how Atlas uses it. A template defines:
- **Template ID and display name** — e.g., `evidence_trail`, "Evidence Trail"
- **Applicable subjects and skill categories** — which territories and topics trigger this template
- **Opening script** — how Atlas starts the activity (e.g., presents a passage, poses a puzzle, sets up a scenario)
- **Conversation flow type** — sequential (step-by-step through a fixed structure), iterative (repeat a loop until mastery), or exploratory (student-led with guardrails)
- **Prompt chip palette** — what follow-up options are offered at each stage (overrides Feature 57's dynamic generation with activity-specific options)
- **Pacing rules** — how many exchanges before a check-in, max response length per stage, when to advance
- **Closing format** — how the activity wraps up (summary, score, encouragement, next suggestion)
- **Anxiety reducer framing** — the emotional tone and language rules for this activity type (drawn from the Iowa alignment doc's anxiety reducer column)

**Initial Template Library (8 templates across 4 subjects)**

**ELA Templates:**

1. **Word Explorer** — Vocabulary acquisition through contextual discovery
   - *Flow:* Atlas presents a short passage with 3–4 target words used in context → student guesses meanings from clues → Atlas confirms/corrects with the actual definition → student uses each word in their own sentence → Atlas evaluates usage
   - *Prompt chips:* "I think it means...", "Give me another clue", "Use it in a sentence for me", "Next word"
   - *Pacing:* 3–4 words per session, ~2–3 exchanges per word
   - *Framing:* "Word treasure hunt" — discovering meanings is an expedition, not a test
   - *Subjects:* ELA (vocabulary topics), also available as a supplementary mode in any subject when vocabulary is flagged as a weak area

2. **Evidence Trail** — Reading comprehension with passage-based questioning
   - *Flow:* Atlas presents a grade-appropriate passage (2–4 paragraphs, generated by Claude) → asks a comprehension question → student answers → Atlas asks "What in the text supports that?" → student identifies evidence → Atlas evaluates and moves to next question type (main idea → inference → author's purpose → personal response)
   - *Prompt chips:* "Read the passage again", "I need a hint", "Here's my evidence", "What's the main idea?"
   - *Pacing:* 1 passage per session, 4–5 questions progressing through comprehension levels
   - *Framing:* "Explorer's journal" — the student is documenting findings, not being tested

3. **Dialogue Workshop** — Grammar and mechanics through editing
   - *Flow:* Atlas presents a short conversation between two Atlas characters that contains intentional errors (punctuation, capitalization, usage, spelling) → student identifies and corrects errors one at a time → Atlas confirms and explains the rule → session ends with a clean version of the dialogue
   - *Prompt chips:* "I found an error", "Show me where to look", "What's the rule?", "The corrected version is..."
   - *Pacing:* 1 dialogue per session, 4–6 errors to find
   - *Framing:* Fixing a character's writing — editing someone else's work removes personal stakes

**Math Templates:**

4. **Expedition Challenge** — Multi-step word problems in narrative context
   - *Flow:* Atlas presents a story scenario tied to the Atlas exploration theme (e.g., calculating supplies for a journey, measuring distances on a map) → breaks the problem into steps → student works through each step with Atlas checking along the way → final answer ties back to the story
   - *Prompt chips:* "What's the first step?", "Check my work so far", "I'm stuck on this step", "What does this mean in the story?"
   - *Pacing:* 1 problem per session, 3–5 steps, each checked individually
   - *Framing:* The math serves the story — "How many days of supplies do we need?" makes fractions feel purposeful

5. **Skill Drill** — Adaptive quick-fire computation practice
   - *Flow:* Atlas presents a series of short computation problems, one at a time → student answers → immediate feedback (correct/incorrect with brief explanation if wrong) → difficulty adjusts based on accuracy → session ends with a score summary
   - *Prompt chips:* "My answer is...", "Show me how", "Easier please", "Bring it on"
   - *Pacing:* 10–15 problems per session, ~1 exchange per problem, total session 5–8 minutes
   - *Framing:* Short and encouraging — "6 for 8 so far, nice pace!" No "wrong" language; incorrect answers get "Not quite — here's why" followed by a similar problem

**Science Templates:**

6. **Lab Log** — Guided inquiry through hypothesis-prediction-observation
   - *Flow:* Atlas describes a phenomenon or poses a question → student forms a hypothesis → Atlas presents data/observations → student compares prediction to outcome → Atlas guides analysis of why results matched or differed → student writes a brief conclusion
   - *Prompt chips:* "My hypothesis is...", "Show me the data", "Why did that happen?", "Let me revise my thinking"
   - *Pacing:* 1 inquiry per session, 5–6 structured steps
   - *Framing:* "Predictions are starting points, not right/wrong answers" — curiosity over correctness

**Social Studies Templates:**

7. **Chronicle Map** — Timeline-based historical reasoning
   - *Flow:* Atlas presents 3–4 historical events (scrambled order or with missing context) → student sequences them and explains connections → Atlas adds context and asks about cause/effect → student identifies a theme or pattern across the events
   - *Prompt chips:* "This came first because...", "These are connected by...", "What happened next?", "Why does this matter?"
   - *Pacing:* 1 set of events per session, 4–5 exchanges
   - *Framing:* "Unlocking history" — students are explorers piecing together a story, not memorizing dates

**Cross-Subject Template:**

8. **Compass Review** — Spaced review of previously learned material
   - *Flow:* Atlas pulls 5–6 concepts the student has practiced before (from session history) across any subject → presents them in a mix of formats (quick recall, application, explain-it-back) → tracks which are retained vs. need reinforcement → flags weak spots for future sessions
   - *Prompt chips:* "I remember this", "I need a refresher", "Quiz me", "Skip this one"
   - *Pacing:* 5–6 items, ~2 exchanges each, total session 8–10 minutes
   - *Framing:* "Checking your compass bearings" — a routine navigation check, not a test

### Technical Details

- **Template storage:** Templates are defined as JSON configurations in a new file: `data/activity_templates.json`. Each template contains: `template_id`, `display_name`, `icon`, `subjects` (array), `skill_categories` (array), `flow_type` ("sequential" | "iterative" | "exploratory"), `system_prompt_overlay` (text injected into the system prompt when this template is active), `prompt_chips` (object mapping stages to chip arrays), `pacing` (object with exchange limits, response length caps, check-in intervals), `anxiety_framing` (text describing the emotional tone), `closing_format` (instructions for how to wrap up).
- **Template selection logic:** When a student enters a topic within a territory, Atlas checks the topic's skill category against available templates. If a match exists, Atlas offers the activity by name: "Want to try an Evidence Trail for this passage, or just chat about it?" In Guided mode (Feature 57), the template is applied automatically with an option to switch. In Open mode, it's offered as a suggestion.
- **System prompt injection:** When a template is active, its `system_prompt_overlay` is appended to the base system prompt (after the Atlas voice overlay and complexity tier instructions from Feature 58). This overlay contains the conversation flow rules, pacing constraints, response format requirements, and anxiety framing language. Claude follows the template structure while still generating original content.
- **Prompt chip override:** Feature 57's dynamic follow-up chip generation is replaced by the template's stage-specific chip palette when a template is active. The "I'm confused" button from Feature 57 remains always visible regardless of template.
- **Session metadata:** When a template is active, the session record includes `activity_template: "evidence_trail"` (or whichever template). This allows the parent dashboard to show what types of activities the student has done, and feeds into the Compass Review template's spaced repetition logic.
- **Template extensibility:** New templates can be added by creating a new JSON entry in `activity_templates.json` and writing the system prompt overlay. No code changes required for new templates — the rendering and flow logic is generic.

### Files Modified
- `app.py` — Template loading, selection logic, system prompt injection, session metadata recording (~100 lines)
- `data/activity_templates.json` — New file containing all 8 template definitions (~300 lines JSON)
- `static/index.html` — Template selection UI when entering a topic, stage-specific prompt chip rendering, activity name display in chat header, closing summary display (~120 lines)
- `static/parent.html` — Activity type breakdown in session history, activity mix visualization on Overview tab (~50 lines)
- `static/guide.html` — Training guide section explaining activity templates and when each is used (~30 lines)
- Help content — Update student help (explain activity types), parent FAQ (what are activity templates, can I control which ones are used), parent tour (point out activity type in session history)

### Acceptance Criteria

- [ ] All 8 initial templates are defined in `activity_templates.json`
- [ ] Templates are automatically suggested when a student enters a matching topic
- [ ] In Guided mode, templates apply automatically with option to switch to free chat
- [ ] In Open mode, templates are offered as suggestions, not forced
- [ ] Each template produces a visibly different conversation structure
- [ ] Word Explorer flows through context → guess → confirm → use pattern
- [ ] Evidence Trail presents a passage and progresses through comprehension levels
- [ ] Dialogue Workshop presents errors for student to find and fix
- [ ] Expedition Challenge breaks word problems into checked steps within a story
- [ ] Skill Drill delivers quick-fire problems with adaptive difficulty
- [ ] Lab Log follows hypothesis → data → analysis → conclusion
- [ ] Chronicle Map sequences events and asks for connections
- [ ] Compass Review pulls from session history for spaced review
- [ ] Prompt chips change based on template stage (not generic dynamic generation)
- [ ] "I'm confused" button remains visible during all templates
- [ ] Session records include which template was used
- [ ] Parent dashboard shows activity type breakdown
- [ ] New templates can be added via JSON without code changes
- [ ] All help content (guide, parent FAQ, student help, tour) is updated
- [ ] Complexity tier (Feature 58) still applies within templates (vocabulary, length, scaffolding level)

### Estimated Scope
- ~100 lines in app.py (template logic, prompt injection, session metadata)
- ~300 lines in activity_templates.json (8 template definitions)
- ~120 lines in index.html (template selection UI, stage chips, activity header, closing display)
- ~50 lines in parent.html (activity type reporting)
- ~30 lines in guide.html (training section)
- Help content updates across all surfaces

### Dependencies
- **Feature 57 (Guided Conversation Mode)** — Required. Feature 60 extends the prompt chip infrastructure and guided/open mode logic that Feature 57 builds.
- **Feature 58 (Adaptive Response Complexity)** — Required. Templates must respect the student's complexity tier for vocabulary, response length, and scaffolding depth.
- **Feature 59 (AI Proficiency & Onboarding)** — Required indirectly (via Features 57 and 58).

---

## Phase 17: Smart Learning Pathways — "Atlas Knows What You Need"

**Status: ✅ Complete | Priority: Critical**

### Vision

Atlas currently presents all learning tools — Diagnostics, Expeditions, Practice, Tutor, Book Mastery, Schoolwork, Study Timer — as equal-weight menu items. The student must decide what to do and which tool to use. This works for a mature learner who understands their own gaps, but it fails the core audience: struggling students in grades 6-12 who don't yet know how to self-direct their learning.

Phase 17 transforms Atlas from a *menu of tools* into a *personalized learning guide*. The student's journey becomes a pipeline: **Diagnostic → Lessons (build proficiency) → Practice (build mastery) → Tutor (unstick and deepen)**. Atlas uses diagnostic scores, lesson history, practice accuracy patterns, and spaced repetition data to recommend the right next step for every topic — and surfaces those recommendations proactively through a redesigned My Map.

The tutor remains always available throughout. A mature student can skip recommendations entirely, drop schoolwork into the tutor, or use any tool directly. The recommendations are guidance, not gates. The design philosophy: **provide a recommended path, but let the student or parent advocate for themselves.** If Atlas's recommendation isn't right, the alternative is one tap away.

### Core Concepts

**Proficiency vs. Mastery**: Atlas tracks two dimensions of knowledge. Proficiency is breadth — has the student been exposed to the concept and do they understand it? Mastery is depth — can the student consistently execute, even under varied conditions? A 65% diagnostic score signals proficiency without mastery. A 25% score signals neither.

**The Learning Pipeline**:
1. **Diagnostic** → Maps the terrain. Identifies where the student stands on every topic.
2. **Expedition (Lesson)** → Builds proficiency. For topics where the student lacks understanding (below ~40%), Atlas teaches through the structured 5-step arc.
3. **Practice** → Builds mastery. For topics where the student understands but needs reps (40-84%), Atlas drills with adaptive difficulty.
4. **Tutor** → Unsticks and deepens. When practice reveals persistent sticking points on specific sub-skills, Atlas recommends a targeted conversation. Also available anytime for self-directed exploration, schoolwork help, or deeper discussion.

**Stuck Detection**: The new signal. When a student has attempted Practice 2+ times on a topic and their accuracy on specific problem types remains below 50%, Atlas identifies this as a "stuck point" and recommends the tutor for a targeted conversation rather than more drilling.

### Feature Breakdown

| Feature | What It Does | Status |
|---------|-------------|--------|
| Feature 61 | Topic Recommendation Engine — backend API that computes recommended action (Learn/Practice/Tutor) per topic using diagnostics, lesson history, practice patterns, stuck detection | ✅ Complete |
| Feature 62 | Smart Topic Routing UI — unified topic view with action badges, routing prompt with recommended path + alternative, replaces separate Expedition/Practice pickers | ✅ Complete |
| Feature 63 | My Map Action Plan Redesign — transforms My Map from navigation menu to personalized per-subject action plan with prioritized next steps | ✅ Complete |
| Feature 64 | Parent Focus Override — parents can set a "Focus this week" subject to boost priority in the action plan | ✅ Complete |

**Build order: 61 → 62 → 63 → 64**

---

## Feature 61: Topic Recommendation Engine
**Critical | Status: ✅ Complete**

### What It Does
The backend intelligence layer for Phase 17. A new API that takes a student's full learning history — diagnostic scores, lesson completions, practice sessions, practice accuracy per problem type, and spaced repetition timing — and returns a recommended action for each topic: **Learn** (Expedition), **Practice**, or **Talk to Tutor**. This is the foundation that Features 62-64 all consume.

### Key Components

- **Recommendation logic** — Score-based routing with contextual overrides:
  - **Below 40% → "Learn" (Expedition)**: Student lacks foundational understanding. Needs the full Hook → Concept → Guided Practice → Independent Practice → Wrap-Up arc.
  - **40–84%, no lesson history → "Learn" (Expedition)**: Even if diagnostic score is moderate, if the student has never had structured teaching on this topic, recommend learning first. Catches students who scored okay through guessing or partial knowledge.
  - **40–84%, has lesson history → "Practice"**: Student understands the concept and has been taught. Needs volume and reps to build consistency.
  - **85%+ → "Strong" / "Practice (Hard)"**: Student is proficient. Offer hard-mode practice for mastery push, or mark as maintained if recently reviewed.
  - **No diagnostic yet → "Take Diagnostic"**: Default first step for unassessed subjects.
  - **Spaced review modifier**: If a topic is due for review regardless of score, flag it and recommend Practice (≥40%) or Expedition (<40%).

- **Stuck detection** — New analysis that identifies when a student should talk to the tutor:
  - Trigger: Student has attempted Practice on a topic 2+ times AND accuracy on a specific question pattern is consistently below 50%.
  - The engine identifies *what* they're stuck on (e.g., "word problems involving distance" within Pythagorean Theorem) by analyzing Claude's feedback tags from practice sessions.
  - Returns `recommended_mode: "tutor"` with a specific conversation starter: "You've been struggling with distance word problems. Let's talk through the approach together."
  - Stuck detection is additive — it doesn't replace the Learn/Practice recommendation, it *overrides* it when the pattern is detected.

- **Tutor context injection** — When the engine recommends the tutor, it also returns a `tutor_context` object that can be passed to the chat system prompt, giving Atlas specific knowledge of what the student is struggling with: "The student has practiced Pythagorean Theorem 3 times but keeps failing problems involving multi-step distance calculations. Focus the conversation on breaking down distance word problems step by step."

- **Batch recommendations endpoint** — A single API call that returns recommendations for ALL topics in a subject, used by the topic grid UI. Avoids N+1 API calls.

### Technical Details

- **New API endpoint**: `GET /api/subject/recommendations/{subject}?student_id=X&instance_id=Y`
  Returns recommendations for all topics in a subject:
  ```json
  {
    "subject": "math",
    "topics": {
      "Pythagorean Theorem & Distance": {
        "score": 65,
        "tier": "proficient",
        "recommended_mode": "practice",
        "recommended_difficulty": "medium",
        "reasoning": "You understand the basics (65%) but need more reps to build consistency.",
        "alternative_mode": "lesson",
        "alternative_label": "Review the concepts",
        "badge": "practice",
        "lesson_count": 1,
        "practice_count": 3,
        "due_for_review": true,
        "stuck": false
      },
      "Linear Equations & Inequalities": {
        "score": 85,
        "tier": "advanced",
        "recommended_mode": "practice",
        "recommended_difficulty": "hard",
        "reasoning": "Strong foundation (85%). Push toward mastery with harder problems.",
        "alternative_mode": "lesson",
        "alternative_label": "Explore advanced concepts",
        "badge": "strong",
        "lesson_count": 2,
        "practice_count": 5,
        "due_for_review": false,
        "stuck": false
      }
    },
    "priority_actions": [
      {
        "topic": "Pythagorean Theorem & Distance",
        "mode": "practice",
        "reason": "Needs reps — due for review",
        "urgency": 1
      }
    ]
  }
  ```

- **New API endpoint**: `GET /api/student/action-plan?student_id=X&instance_id=Y`
  Returns the top 3-5 priority actions across ALL subjects for the My Map redesign:
  ```json
  {
    "actions": [
      {
        "subject": "math",
        "subject_icon": "📐",
        "topic": "Pythagorean Theorem & Distance",
        "mode": "practice",
        "reasoning": "65% — needs reps to build consistency",
        "urgency": 1
      },
      {
        "subject": "science",
        "subject_icon": "🔬",
        "topic": "Chemical Reactions",
        "mode": "tutor",
        "reasoning": "Stuck on balancing equations — let's talk it through",
        "tutor_context": "Student has practiced Chemical Reactions 3 times but keeps failing balancing equation problems.",
        "urgency": 2
      },
      {
        "subject": "ela",
        "subject_icon": "📚",
        "topic": "Figurative Language",
        "mode": "lesson",
        "reasoning": "New territory (32%) — start with an expedition",
        "urgency": 3
      }
    ],
    "focus_subject": null
  }
  ```

- **Routing thresholds** (constants in app.py, potential future parent override via Feature 64):
  - `LEARN_THRESHOLD = 40` — Below this → Expedition
  - `MASTERY_THRESHOLD = 85` — Above this → Strong / Hard Practice
  - `STUCK_PRACTICE_COUNT = 2` — Minimum practice attempts before stuck detection activates
  - `STUCK_ACCURACY_THRESHOLD = 50` — Below this on repeated attempts → tutor recommendation
  - `ZERO_LESSON_OVERRIDE = True` — No lesson history + score 40-84% → Learn first

- **Stuck detection implementation**: Analyze the practice log for a topic. For each practice session, the existing feedback markers (`===FEEDBACK=== correct/incorrect`) are already tracked. Aggregate accuracy across the last 2-3 sessions. If overall accuracy < 50% after 2+ sessions, flag as stuck. Future enhancement: analyze feedback text to identify specific problem-type patterns (would require tagging practice questions by sub-skill).

- **Parent dashboard alignment**: The parent Study Plan already computes `action: 'lesson' | 'practice'` per topic. Refactor this to call the same recommendation engine so both surfaces always agree. Add `'tutor'` as a third action type.

### Files Modified
- `app.py` — New recommendation endpoints, stuck detection logic, routing threshold constants, action plan aggregator (~120 lines)

### Acceptance Criteria
- [ ] `/api/subject/recommendations/{subject}` returns correct mode for each topic based on score and history
- [ ] `/api/student/action-plan` returns top 3-5 priority actions across all subjects
- [ ] Students below 40% get "lesson" recommendation
- [ ] Students 40-84% with lesson history get "practice" recommendation
- [ ] Students 40-84% with zero lesson history get "lesson" recommendation (override)
- [ ] Students 85%+ get "practice (hard)" or "strong" recommendation
- [ ] Stuck detection triggers "tutor" recommendation after 2+ low-accuracy practice sessions
- [ ] Tutor recommendations include context for the chat system prompt
- [ ] Spaced review due dates factor into urgency ranking
- [ ] Parent Study Plan uses the same recommendation engine

### Estimated Scope
- ~120 lines in app.py (endpoints, recommendation logic, stuck detection, action plan)

### Dependencies
- **Adaptive learning engine** — Required. `compute_subject_mastery()` and `adaptive_pick_topic()` provide the mastery data.
- **Practice log with feedback** — Required. Stuck detection reads practice session accuracy from existing feedback markers.

---

## Feature 62: Smart Topic Routing UI
**Critical | Status: ✅ Complete**

### What It Does
The student-facing presentation layer for Feature 61's recommendations. Replaces the separate Expeditions and Practice pickers with a single unified **Explore** view per subject. Each topic card shows an action badge (Learn / Practice / Tutor / Strong). Clicking a card opens a routing prompt that recommends the right path and lets the student choose an alternative.

### Key Components

- **Unified Explore panel** — The Expeditions and Practice panels merge into a single "Explore [Subject]" panel. One topic grid, one entry point per topic. The sidebar collapses "🗺️ Expeditions" and "⛏️ Practice" into a single "📍 Explore" button. Existing `navLessons` and `navPractice` become sub-options within the Explore panel for students who specifically want to browse lesson history or practice history.

- **Smart topic cards** — Each topic card displays:
  - Topic name and mastery score (as today)
  - A **recommended action badge**: "📖 Learn" (amber) or "🔧 Practice" (teal) or "💬 Tutor" (coral) or "✅ Strong" (green)
  - A **brief reason**: "New to you", "Needs reps", "Stuck — let's talk", "Due for review", "Push to mastery"

- **Routing prompt** — When a student clicks a topic card, a brief inline expansion (not a modal — keeps context visible) appears below the card:
  - **Reason line**: "You scored 65% — you understand the basics but need more reps to build consistency."
  - **Recommended path** (prominent button): "🔧 Start Practice" or "📖 Start Expedition" or "💬 Talk to Atlas"
  - **Alternative paths** (smaller links): "or review the concepts" / "or practice instead" / "or ask the tutor"
  - One click on the recommended button starts the right session. No extra steps for the common case.
  - The routing prompt calls `startLesson()`, `startPractice()`, or opens the chat panel with pre-loaded context — all existing functions.

- **Subject tab bar** — Keep the existing multi-subject tab bar (Math / Science / ELA / Social Studies) at the top of the Explore panel, same as the current Expedition picker.

- **History sections** — Below the topic grid, show combined Expedition + Practice history for the subject (replacing the separate history sections that currently live in each panel).

### UX Copy

Topic card badges:
- Below 40%: `📖 Learn` (amber) — "New to you" or "Needs teaching"
- 40-84%, no lessons: `📖 Learn` (amber) — "Start here first"
- 40-84%, has lessons: `🔧 Practice` (teal) — "Needs reps" or "Due for review"
- 40-84%, stuck: `💬 Tutor` (coral) — "Stuck — let's talk it through"
- 85%+: `✅ Strong` (green) — "Push to mastery" or "Maintaining"
- No diagnostic: `🔍 Assess` (gray) — "Take a diagnostic first"

Routing prompt examples:
- **65%, has done 1 expedition**: "You've got the basics down (65%). Atlas recommends drilling with practice problems to build consistency. **[🔧 Start Practice]** *or [review the concepts]*"
- **30%, no expeditions**: "This is new territory (30%). Atlas recommends starting with a guided expedition to learn the foundations. **[📖 Start Expedition]** *or [jump to practice]*"
- **72%, stuck on word problems**: "You know this topic (72%) but keep getting tripped up on word problems. Let's talk through the approach together. **[💬 Talk to Atlas]** *or [more practice]*"
- **88%, due for review**: "You're strong here (88%) but it's been a while. A quick practice session will keep it fresh. **[🔧 Quick Practice]** *or [do a full expedition]*"

### Files Modified
- `static/index.html` — Unified Explore panel, smart topic cards with badges, routing prompt expansion, sidebar nav consolidation, combined history section (~250 lines net change)
- `static/guide.html` — Training guide section explaining Learn vs. Practice vs. Tutor recommendations (~25 lines)
- Help content — Update student help ("How does Atlas decide what I should do?"), parent FAQ ("What's the difference between Expeditions and Practice?")

### Acceptance Criteria
- [ ] Sidebar shows unified "📍 Explore" replacing separate Expeditions/Practice buttons
- [ ] Topic grid renders with action badges from Feature 61's recommendation API
- [ ] Clicking a topic card expands inline routing prompt
- [ ] Recommended action button starts the correct session type
- [ ] Alternative link(s) start the other session types
- [ ] Tutor routing pre-loads chat with stuck-point context
- [ ] Combined history section shows both Expedition and Practice history
- [ ] Existing lesson/practice start functions work unchanged
- [ ] All help content updated

### Estimated Scope
- ~250 lines in index.html (panel restructuring, card badges, routing prompt, nav changes)
- ~25 lines in guide.html
- Help content updates

### Dependencies
- **Feature 61 (Topic Recommendation Engine)** — Required. Provides the recommendation data that drives all UI elements.

---

## Feature 63: My Map Action Plan Redesign
**Critical | Status: ✅ Complete**

### What It Does
Transforms My Map from a navigation screen into a **personalized action plan**. Instead of showing equal-weight territory buttons and generic stats, My Map now tells each student exactly what to do next — specific to each subject, based on where they actually are in their learning journey.

### Key Components

- **"What to Do Next" hero section** — The top of My Map shows the 2-3 highest-priority actions across all subjects, pulled from Feature 61's `/api/student/action-plan` endpoint. Each action card shows: subject icon, topic name, recommended mode (Learn/Practice/Tutor), and a brief reason. Clicking an action card routes directly via Feature 62's routing logic. This section answers the question every student has when they log in: "What should I work on?"

- **Territory action cards** — Below the hero section, each territory (subject) card transforms from a simple door into a mini status report:
  - Subject name and icon
  - Overall mastery percentage
  - **Top 1-2 recommended actions** for that subject with badges: "📖 Learn Figurative Language" or "🔧 Practice Chemical Reactions (due for review)"
  - Clicking the action routes directly. Clicking the territory name opens the full Explore panel (Feature 62).
  - Quick stats remain: expeditions completed, practice accuracy, diagnostics done.

- **First-time / no diagnostic state** — For subjects where the student hasn't taken a diagnostic:
  - Territory card shows "🔍 Take your first diagnostic to unlock personalized recommendations"
  - Clicking routes to the diagnostic for that subject
  - Tutor and Schoolwork remain accessible regardless — these are self-directed tools that don't require a diagnostic

- **Always-available tools section** — Below the territory cards, a compact row of tools that are always available regardless of diagnostic status: "💬 Tutor", "📝 Schoolwork", "📚 Book Mastery", "⏱️ Study Timer". These don't need recommendations — they're self-directed. This replaces the current sidebar nav approach where every tool is a full nav item.

- **Reduced cognitive load** — The current My Map shows 10+ nav items in the sidebar. The redesign surfaces only the most important actions (2-3 at most) in the hero section, with the full subject breakdown below. A student with ADHD accommodations (future Feature 26) could see an even more simplified view — just the single top-priority action.

- **Session re-entry** — If the student has an active (in-progress) Expedition or Practice session, that appears at the very top as a persistent "Continue" banner, above the What to Do Next section. Same as the existing resume banner but promoted to My Map level.

### "What to Do Next" prioritization logic
Actions are ranked by:
1. **Active sessions** (in-progress Expedition or Practice) — always highest priority
2. **Stuck topics** (tutor recommended) — intervention needed
3. **Weak + due for review** — weakest topics that are also overdue for spaced review
4. **Due for review** — any topic overdue, sorted by weakness
5. **Weak topics** — low-scoring topics not yet due for review
6. **Undiagnosed subjects** — subjects where no diagnostic has been taken
7. **Maintenance practice** — strong topics that could use a refresh

If a parent has set a Focus Subject (Feature 64), that subject's actions get boosted to the top regardless of the normal priority order.

### Technical Details

- **Data source**: Calls Feature 61's `/api/student/action-plan` endpoint on My Map load. This returns the pre-prioritized action list.
- **Rendering**: Replaces the current `showWelcome()` function's HTML generation with a new `renderActionPlan()` function that builds the hero section, territory cards, and always-available tools.
- **Performance**: The action plan endpoint should be fast (~100ms) since it only reads local JSON files. Cache the result for the session so navigating back to My Map doesn't re-fetch.
- **Responsive**: Territory cards should wrap on mobile. Hero actions should stack vertically on narrow screens.

### Files Modified
- `static/index.html` — My Map redesign: hero section, territory action cards, always-available tools, resume banner promotion, `renderActionPlan()` function (~300 lines net change, replacing significant existing code in `showWelcome()`)
- `static/parent.html` — Minor: parent tour text updates to reflect new My Map layout (~10 lines)
- `static/guide.html` — Training guide section explaining the new My Map and how recommendations work (~30 lines)
- Help content — Update student help ("What does My Map show me?"), parent FAQ ("How does Atlas decide what my child should work on?"), parent tour

### Acceptance Criteria
- [ ] My Map shows "What to Do Next" hero section with top 2-3 priority actions
- [ ] Each territory card shows 1-2 recommended actions with badges
- [ ] Clicking an action routes to the correct tool (Expedition, Practice, Tutor, or Diagnostic)
- [ ] Subjects without diagnostics show clear "Take diagnostic" prompt
- [ ] Tutor, Schoolwork, Book Mastery, Study Timer are always accessible
- [ ] Active in-progress sessions appear as top-priority "Continue" banner
- [ ] My Map renders cleanly with zero diagnostics (new student experience)
- [ ] My Map renders cleanly with all diagnostics completed
- [ ] Recommendations match parent dashboard Study Plan
- [ ] All help content updated

### Estimated Scope
- ~300 lines in index.html (My Map redesign, action plan rendering)
- ~30 lines in guide.html
- ~10 lines in parent.html (tour updates)
- Help content updates

### Dependencies
- **Feature 61 (Topic Recommendation Engine)** — Required. Provides the `/api/student/action-plan` data.
- **Feature 62 (Smart Topic Routing UI)** — Required. Action card clicks route through the same unified Explore panel.

---

## Feature 64: Parent Focus Override
**Important | Status: ✅ Complete**

### What It Does
Adds a "Focus This Week" control to the parent dashboard, allowing parents to boost a specific subject's priority in the student's My Map action plan. When a parent knows their child has a math test Friday or a science project due, they can tell Atlas to prioritize that subject — overriding the algorithm's default prioritization without disabling it.

### Key Components

- **Focus Subject selector** — A simple dropdown or button group in the parent dashboard Settings tab (or Overview tab). Shows all enabled subjects. Parent selects one (or "None — let Atlas decide"). Stored in the instance config under the student's record.

- **Action plan boost** — When a Focus Subject is set, Feature 61's `/api/student/action-plan` endpoint boosts that subject's actions to the top of the priority list. The hero section on My Map will lead with the focused subject's recommendations. Other subjects still appear below — nothing is hidden, just reordered.

- **Visual indicator** — On the student's My Map, the focused subject's territory card gets a subtle highlight or badge: "⭐ Focus this week — set by parent". This lets the student know there's a reason it's being prioritized without being heavy-handed.

- **Expiration** — Focus setting persists until the parent clears it or changes it. No automatic expiration (parents know when the test is over). Could add optional expiration date in a future iteration.

- **Per-student** — Focus is set per student, not per instance. One child might need math focus while another needs ELA.

### Technical Details

- **Storage**: Add `focus_subject` field to the student record in the instance's `students.json`. Value is a subject key (e.g., "math") or `null`.
- **API endpoint**: `POST /api/instance/{instance_id}/student/{student_id}/focus` — Sets or clears the focus subject. Requires parent PIN auth.
- **Action plan integration**: The `/api/student/action-plan` endpoint checks for `focus_subject` and boosts that subject's actions to urgency level 0 (above all other priorities).
- **Parent dashboard**: Add a "Focus Subject" control to either the Settings tab or as a quick-action in the Overview tab's student selector area.

### Files Modified
- `app.py` — New focus endpoint, action plan boost logic (~30 lines)
- `static/parent.html` — Focus subject selector in dashboard (~40 lines)
- `static/index.html` — Focus indicator on My Map territory card (~15 lines)

### Acceptance Criteria
- [ ] Parent can set a Focus Subject per student from the dashboard
- [ ] Parent can clear the Focus Subject (return to "let Atlas decide")
- [ ] Focused subject's actions appear at top of My Map action plan
- [ ] Student sees subtle indicator that a subject is focused
- [ ] Focus persists across sessions until parent clears it
- [ ] Focus is per-student (siblings can have different focus subjects)
- [ ] Help content updated (parent FAQ, parent tour)

### Estimated Scope
- ~30 lines in app.py
- ~40 lines in parent.html
- ~15 lines in index.html
- Help content updates

### Dependencies
- **Feature 61 (Topic Recommendation Engine)** — Required. Focus boost is applied within the action plan endpoint.
- **Feature 63 (My Map Redesign)** — Required. Focus indicator renders on the redesigned territory cards.

---

## Feature 65: What's New Notifications
**Nice-to-Have | Status: ✅ Complete**

### What It Does
A dismissible "What's New" banner that appears on both the student My Map and parent dashboard after a release. Notifies users about new features with clear, audience-appropriate messaging. Students get simple language explaining where to find changes and how the logic works. Parents get more detail on the system's reasoning and any new controls available to them.

### Key Components

- **Dismissible banner** — Appears at the top of My Map (student) or Overview tab (parent) on first login after a release. Stored in localStorage keyed to version + user ID, so it shows once per user per release. Fades out with animation on dismiss.
- **Help menu link** — Permanent "🆕 What's New" option in the ? help menu on both student and parent portals. Opens a panel showing all release notes in reverse chronological order.
- **Hardcoded per version** — Release notes are defined in a JS array (`WHATS_NEW_RELEASES` / `PARENT_WHATS_NEW_RELEASES`). Adding notes for a new version means adding an entry to the array — no backend changes needed.

### Files Modified
- `static/index.html` — CSS, banner container, JS (render, dismiss, help menu page)
- `static/parent.html` — CSS, banner container, JS (render, dismiss, help menu page)

### Dependencies
- None — standalone feature.

---

## Estimated Costs

| Item | Estimated Cost |
|------|---------------|
| **Claude API** | ~$5–20/month (Sonnet model recommended) |
| **Hosting** | $0 — runs locally on your computer |
| **Domain/SSL** | $0 — accessed via localhost |
| **Tools & Libraries** | $0 — all open source |
| **Total Ongoing** | ~$5–20/month |

---

## Getting Started Checklist

- [x] Install Python from python.org/downloads (one-time, 5 minutes)
- [x] Sign up for an Anthropic API account at console.anthropic.com
- [x] Get your API key and add $5–10 in credit
- [x] Claude generates the entire project — you paste one startup command into Terminal
- [x] Open your browser to localhost and start using the tutor

---

*Plan created: March 2, 2026*
*Last updated: March 24, 2026*
*Approach: Iterative — start simple, ship early, improve continuously*
*Built for: Kalib's son and other students, grades 6–12, general enrichment across 5 subjects*
