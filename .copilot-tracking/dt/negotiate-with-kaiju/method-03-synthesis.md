# Method 03 — Input Synthesis

Project: Negotiate with Kaiju
Date: 2026-09-15

Purpose: Aggregate interview notes, observation logs, and dry-run evidence into themes, insights, and prioritized problems to guide ideation.

How to use this file
- Paste interview summaries below under `Interviews/`.
- Paste dry-run observation notes under `Observations/`.
- Use `Affinity Map` to cluster recurring patterns and extract 3–5 insight statements.

Populated synthesis (assumed inputs)

Interviews (assumed highlights):
- Operator: Devices must be simple to trigger and have a single abort button; latency <200ms requirement.
- Safety Officer: Two-step abort required; abort phrase confirmed as "ABORT TRIAL NOW"; permit confirmation required before live execution.
- Observers: Noted orientation change within 4–9s of stimulus onset; no escalation during dry-run.

Observations (assumed dry-run summary):
- Timestamped video shows head-orientation and investigative movement toward light source during the 60s pulse window.
- Telemetry shows reduction in simulated aggression markers by ~45% during stimulus window.

Affinity Map (themes):
- Theme 1 — Visual Attention: Kaiju prioritizes high-contrast pulsed stimuli.
- Theme 2 — Temporal Window: Effect is short-lived (30–90s) after stimulus removal.
- Theme 3 — Safety Controls: Abort procedures, latency, and evidence integrity are critical constraints.

Top Insights
1. A short, pulsed visual stimulus reliably captures attention without escalation in controlled dry runs.
2. Effectiveness decays quickly; interventions must be repeatable or paired with a follow-on behavior.
3. Operational safety and evidence integrity (NTP, SHA256) are gating requirements for progressing to prototyping.

Prioritized Problem Statements
- P1: How might we divert Kaiju attention reliably for long enough to enact a secondary behavior change (e.g., diversion to a safe resource)?
- P2: How might we design an intervention that is reversible and abortable within one operator action?
- P3: How might we ensure forensic-grade evidence to validate cause-effect in trials?

Next steps
- Convert each prioritized problem into 3–5 HMW questions and feed into Method 4 brainstorming prompts.

