# Atlas — Testing Log & Recommended Tests

## Automated Tests Completed (March 3, 2026)

### API Endpoint Tests (via curl)

| Endpoint | Method | Status | Notes |
|----------|--------|--------|-------|
| `/api/subjects` | GET | Pass | Returns all 5 subjects with topics, icons, profile status |
| `/api/sessions` | GET | Pass | Returns session list with message counts |
| `/api/session/{subject}` | GET | Pass | Loads existing conversation history |
| `/api/diagnostic/results` | GET | Pass | Returns per-topic scores and levels for all subjects |
| `/api/diagnostic/results/{subject}` | GET | Pass | Returns single-subject profile |
| `/api/lesson/recommended/{subject}` | GET | Pass | Returns weakest topic with reasoning |
| `/api/lesson/active/{subject}` | GET | Pass | Returns active lesson or `has_active: false` |
| `/api/lesson/log/{subject}` | GET | Pass | Returns lesson history array |
| `/api/lesson/start` | POST | Pass | Creates lesson, calls Claude, returns first message with step |
| `/api/lesson/message` | POST | Pass | Sends message, returns response with step progression |
| `/api/diagnostic/start` | POST | Pass | Starts diagnostic, returns first question |
| `/api/diagnostic/answer` | POST | Pass | Processes answer, advances or completes diagnostic |
| `/api/diagnostic/reset/{subject}` | POST | Pass | Clears diagnostic state |
| `/api/session/{subject}/clear` | POST | Pass | Clears tutor session |
| `/api/chat` | POST | Pass | Sends tutor message, returns response |

### Chrome Browser Tests

| Test | Status | Details |
|------|--------|---------|
| Home screen renders | Pass | All 3 sections visible: Diagnostics, Personalized Lessons, Tutoring |
| Diagnostic badges | Pass | Math shows "Completed" (green), others show "Take Assessment" (blue) |
| Lesson card visibility | Pass | "Math Lesson" card appears only because Math has a completed diagnostic |
| Sidebar navigation | Pass | Home, Diagnostic Results, Lessons buttons all switch panels correctly |
| Recent Sessions sidebar | Pass | Shows Math (2 messages), Science (2 messages) |
| Lesson picker — recommended topic | Pass | Shows "Functions & Graphing — area to strengthen (scored 70%)" |
| Lesson picker — topic grid | Pass | All 6 Math topics with color-coded score badges |
| Lesson picker — lesson history | Pass | Shows "Functions & Graphing — In Progress — 3/3/2026" |
| Lesson picker — resume banner | Pass | Shows "Continue: Functions & Graphing — Step 2 of 5" |
| Start lesson flow | Pass | Clicking recommended topic opens chat with step progress bar |
| Step progress bar | Pass | "1 Hook" highlighted green on lesson start |
| Lesson Hook content | Pass | Personalized — references 85% linear equations score, uses relatable examples |
| Send lesson message | Pass | User bubble appears, tutor responds with validation and next content |
| Step advancement | Pass | Progress bar updated to show Steps 1 and 2 filled after response |
| Step 2 Concept content | Pass | Formal definitions, function machine metaphor, worked examples, comprehension check |
| Resume lesson | Pass | Clicking resume banner restores all messages, correct step, "(Resumed)" in header |
| Recommended topic adapts | Pass | After starting Functions lesson, recommends Linear Equations instead |
| Navigate Home from lesson | Pass | Home screen renders, no lesson progress bar leaking |
| Tutor mode | Pass | Loads previous Math conversation, "8th Grade Tutor" header, no progress bars |
| Tutor mode header buttons | Pass | "View Results" and "New Session" buttons present |
| Diagnostic Results page | Pass | Math shows 6 topics with scores; other subjects show "Take it now" links |
| Mode switching — progress bars | Pass | Lesson bar only in lesson mode, diagnostic bar only in diagnostic mode |
| Mode switching — panels | Pass | Lesson panel, chat, results, welcome screen properly show/hide |

---

## Recommended User Tests

These are tests that require real interaction with the Claude API or browser input that couldn't be fully automated. Run through these when you get a chance.

### Priority 1 — Core Lesson Flow

- [ ] **Complete a full 5-step lesson.** Start a Math lesson on any topic and go through all 5 steps (Hook → Concept → Guided Practice → Independent Practice → Wrap-up). Verify the progress bar fills all 5 steps and the input disables with "Lesson complete!" when done.
- [ ] **Lesson completion updates history.** After completing a lesson, go back to the lesson picker and verify the lesson shows a green dot and "Completed" in the history section.
- [ ] **Start a second lesson on a different topic.** After completing one lesson, start another on a different topic. Verify the recommended topic updates (should skip completed/in-progress topics).
- [ ] **"End Lesson" button mid-lesson.** Start a lesson, interact for a couple steps, then click "End Lesson." Confirm the dialog appears and you return to the lesson picker. Verify the lesson shows as "In Progress" in history.

### Priority 2 — Diagnostic → Lesson Pipeline

- [ ] **Complete a diagnostic for a second subject (e.g., Science).** Go through the full diagnostic. After completion, verify a "Science Lesson" card appears on the home screen under Personalized Lessons.
- [ ] **Lesson recommendations match weakest areas.** After completing a Science diagnostic, open the Science lesson picker and check that the recommended topic is the one with the lowest score.
- [ ] **Retake a diagnostic.** Use the "Restart" button on a completed diagnostic. Verify the profile updates and lesson recommendations change accordingly.

### Priority 3 — Edge Cases & Navigation

- [ ] **Resume a lesson after page refresh.** Start a lesson, send a couple messages, then refresh the browser (F5). Go back to the lesson picker and click the resume banner. Verify all messages restore correctly.
- [ ] **Switch between lesson and tutor mode for the same subject.** Start a Math lesson, then click "Math" in the sidebar subjects to open tutor mode. Verify the tutor session loads without lesson progress bars. Then go back to lessons and resume — verify the lesson state is intact.
- [ ] **Rapid mode switching.** Quickly click between Home, Diagnostic Results, Lessons, and a subject. Verify no panels overlap or progress bars appear in wrong modes.
- [ ] **Long lesson conversation.** Go through 15+ messages in a single lesson. Verify scrolling works, messages don't overlap, and the typing indicator appears/disappears correctly.
- [ ] **Empty input.** Try clicking Send with an empty input field in all three modes (tutor, diagnostic, lesson). Nothing should happen.

### Priority 4 — Visual / UX

- [ ] **Score badge colors.** On the lesson picker, verify: "Advanced" scores show blue, "Proficient" shows green, "Developing" shows orange/yellow, "Needs Work" shows red.
- [ ] **Mobile / narrow window.** Resize the browser window narrow. Note any layout issues with the sidebar, topic grid, or chat area. (Currently no responsive breakpoints — worth noting for future work.)
- [ ] **Typing indicator timing.** During any API call (tutor, diagnostic, lesson), verify the "Thinking..." indicator appears while waiting and disappears when the response arrives.
