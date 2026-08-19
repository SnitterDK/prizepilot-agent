# Four-minute demo script

## 0:00–0:30 — Problem

Show three near-identical application forms. Explain that the dangerous part is
not repetitive typing; it is losing track of eligibility evidence and what the
owner has actually approved.

## 0:30–1:10 — Inputs

Open PrizePilot Agent. Show the opportunity rules and the owner profile as two
separate evidence sources. Emphasize that missing information remains unknown.

## 1:10–2:10 — Autonomous workflow

Run the agent. Show:

1. Google and AWS competitions move to “evidence needed” because repository and
   video links do not exist yet.
2. A student-only competition is blocked because student status is not verified.
3. The audit reason appears beside each decision.

## 2:10–2:50 — Human approval boundary

Explain that an application becomes externally actionable only after the owner
approves the exact destination, data categories and final action. Optional
marketing consent remains separate.

## 2:50–3:30 — Architecture

Show `docs/architecture.svg`. Explain the deterministic gate, provider adapter,
approval checkpoint and audit log. For Google, show the Cloud Run service and
Gemini/ADK call. For AWS, show the Strands execution trace.

## 3:30–4:00 — Value and honesty

State the value without unsupported metrics: one source of truth, fewer repeated
steps, explicit blockers, and safer submissions. Close with the principle:
“Autonomy should remove routine work—not remove informed consent.”

