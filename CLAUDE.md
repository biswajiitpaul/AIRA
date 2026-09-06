# AIRA — Claude Code Master Instructions

You are building **AIRA**, an AI-powered environmental intelligence and early-warning platform for air pollution in Delhi, for the Google Cloud "Build with AI: Code for Communities" hackathon (Track 02: Clean Air & Climate Resilience). Deadline is fixed — work efficiently, not exhaustively.

Read `docs/build-brief.md` and `docs/implementation-plan.md` in this repo before doing anything else if they exist. Everything below governs how you work, not just what to build.

---

## Non-negotiable constraints

1. **Never invent data, API responses, benchmark results, or metrics.** If you can't get real data or can't run a real test, say so explicitly and stop rather than fabricating a plausible-looking result.
2. **ML predicts. Gemini explains.** Never ask Gemini to produce a numerical forecast. Use deterministic/statistical models (regression, z-score, ARIMA, AutoML) for forecasting and anomaly detection. Gemini's job is: image analysis, natural-language explanation of computed results, and reasoning over structured data — not generating numbers from nothing.
3. **Never claim causation from correlation.** Source attribution must use words like "probable" / "suspected contributing factor," never definitive statements like "X caused this."
4. **₹0 budget.** Only use free-tier APIs and public datasets. Flag anything that would require payment instead of silently skipping it.
5. **Keep every external data provider behind an adapter** (`data/adapters/`). Nothing downstream should import provider-specific logic directly.
6. **Never commit API keys or secrets.** Read from environment variables only. If you create a `.env`, immediately confirm it's in `.gitignore`.
7. **Privacy**: no facial recognition, no continuous tracking, citizen photo submission is always optional, never claim access to private/CCTV feeds.
8. **Don't build what's explicitly out of scope**: no blockchain, no drones, no custom LLM training, no physical IoT deployment, no unnecessary chatbot/social features. If a feature doesn't improve detection, prediction, decision-making, or public safety regarding air pollution, don't build it.

---

## The build order (do not reorder or skip ahead)

1. Data ingestion (CPCB/OpenCity Delhi CSV, NASA FIRMS, weather) → normalized schema
2. Anomaly detection + forecasting (simple statistical models first)
3. Risk fusion (transparent, documented formula) + source attribution
4. Gemini integration (explanation generation + citizen photo analysis)
5. Backend API exposing the above
6. Frontend dashboard (can start early against mock JSON matching the real API schema)
7. Incident lifecycle (detected → review → confirmed/rejected → resolved)
8. Demo resilience (cached replay mode using the locked Oct 25–Nov 10, 2019 Delhi dataset)
9. Polish / stretch goals — only if ahead of schedule
10. Submission packaging

Full detail for each phase, including exact file targets and checkpoints, is in `docs/implementation-plan.md`.

---

## The autonomous loop

For each task within a phase, run this loop without waiting for confirmation between steps, **except at the STOP points defined below**:

```
1. CREATE  — write the code for the current, specific task (one module/file at a time, not the whole phase at once)
2. CHECK   — actually run it: execute the script, hit the API endpoint, run the test.
             Show real output, not a description of expected output.
3. FIX     — if it errors or the output looks wrong/implausible, diagnose and fix it yourself, then re-run.
             Repeat CHECK → FIX until it genuinely works, not just until it stops throwing errors.
4. VERIFY  — compare the real output against the phase's stated checkpoint criterion
             (e.g., "does the anomaly detector actually flag Nov 3-5, 2019?").
             If it doesn't meet the checkpoint, treat that as a FIX case, not a pass.
5. LOG     — append a short entry to PROGRESS.md: what was built, what was verified,
             any data quirks or assumptions you had to make.
6. COMMIT  — git commit with a clear message once the checkpoint is genuinely met.
7. NEXT    — move to the next task in the current phase. Only move to the NEXT PHASE
             once every checkpoint in the current phase is met.
```

Keep looping through CREATE → CHECK → FIX → VERIFY autonomously for a given task. Don't ask "should I fix this?" — fix it. Don't ask "does this look right?" — check against the checkpoint yourself and say what you found.

## STOP points — always pause here and ask me directly

- Before using any API key or credential I haven't already provided in `.env`
- Before creating any paid resource, or anything that could incur cost even on a "free tier" if usage grows
- Before deploying anything publicly (Cloud Run, hosting, etc.) — I want to review before it's live
- If real data genuinely isn't obtainable for something the plan assumes is real (e.g., a source is down, requires approval you don't have) — tell me, propose the closest honest alternative, don't silently substitute fabricated data
- Before moving from one phase to the next (quick summary + explicit go-ahead)
- If you've been stuck in FIX on the same task for more than ~3 iterations — stop and explain what's failing rather than continuing to guess

---

## Quality bar for "done"

A task is not done because it stopped erroring. It's done when:
- It runs against real data (not mocks, past Phase 0 setup)
- Its output was actually inspected and matches what the checkpoint requires
- It's committed with a message describing what it does and why

## PROGRESS.md format

Keep a running log at the repo root:
```
## [Date] Phase X - Task name
- What was built
- What was verified (with the actual checked output/number, not "looks good")
- Assumptions or data quirks encountered
- Next task
```

This file is your own memory across sessions — read it at the start of each session before continuing.