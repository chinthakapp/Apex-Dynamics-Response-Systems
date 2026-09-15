Notes on permits and approvals
- Regulatory: Obtain any required city / environmental / airspace permits before scheduling the trial. Do not execute without documented approvals.
- Legal: Ensure insurance and liability coverage is confirmed for the staging site and equipment.

Redundant communications
- Use two independent comms channels: primary secure radio channel (default: Radio 7) and secondary backup (satellite phone or cellular emergency channel). Record call signs.

Data handling and timestamping (best practice)
- Use NTP-synced devices for all cameras and sensors. Store evidence in a centralized, access-controlled evidence bucket (path: `.copilot-tracking/dt/negotiate-with-kaiju/evidence/{trial-id}/`).
- Ensure at least one witness-grade camera (30+ FPS), microphone, and GPS tracker are recording with timestamps.

Staging coordinates (conservative placeholder)
- Computed conservative staging coordinate 15 km north of Redmond city center (use until you provide exact address/staging site):
- LAT: 47.809000, LON: -122.121513 (WGS84) — approximately 15 km north of Redmond center. Trial Lead must confirm coordinates meet clearance and local site suitability.

Operator & training (best practice)
- Device operator must be certified by Ops Lighting Team and briefed on ramp procedures and emergency shutdown. Conduct a dry-run with the operator at T-120m.

# Method 02 — Template Trial Plan (Small, Reversible Diversion)

Purpose: Provide the Chief Negotiator and response team a one-page, executable plan for a controlled diversion trial (light-based) that tests whether a pulsed visual signal shifts Kaiju attention away from the city.

Why: A clear, city-specific plan minimizes risk, aligns responsibilities, and ensures the trial produces interpretable evidence for Method 2 analysis.

Trial Overview
- Trial ID: light-trial-01
- Objective: Test whether a 60s pulsed visual signal at Location A shifts Kaiju attention away from the city perimeter for ≥10 minutes without escalation.

Scope
- Single, short-duration light-based trial. Reversible: lights only; no provisioning.

Inputs (from user / conservative defaults)
- Safe distance from populated areas: 15 km (user input)
- Primary comms & abort phrase: Secure Ops Channel (Radio 7) — abort phrase: "ABORT TRIAL NOW" (conservative default; confirm exact channel)
- Authorization: Project approver (you) — you will authorize prior to T-30m
- Lighting device: tower-mounted floodlight array (user input)
- Device operator: Ops Lighting Team (default team — confirm operator name)
- Max brightness (conservative limit): ≤50,000 lumens (set to avoid blinding or strobe-level intensity)
- Test window: Tentative — within 72 hours / ASAP (default); exact datetime required
- Safety Officer: John Smith (user input)

Roles & Responsibilities
- Chief Negotiator (approver): authorizes trial, monitors translator feedback, can abort.
- Kaiju Translator: confirms signal acceptability and interprets responses.
- Trial Lead (ops): operates lights, enforces device parameters.
- Observers (1+): complete `method-02-observation-checklist.md` and record evidence.
- Safety Officer (John Smith): authority to abort immediately.

Location & Distance
- Site: select a staging site at least 15 km from populated areas and key infrastructure. Exact coordinates to be provided by Trial Lead. (Conservative default: choose a cleared staging area outside the 15 km perimeter and with open sightlines.)

Stimulus Parameters
- Device: tower-mounted floodlight array
- Pattern: 1 Hz pulsed sequence (0.5s on, 0.5s off)
- Duty cycle: 50%
- Duration: 60 seconds total
- Ramp: 0% → 10% over 5s → 50% over next 5s → hold for remaining time
- Color: blue-white (confirm with Translator)

Timeline
- T-60m: Final briefing; confirm roles, comms, abort phrase, evidence capture location
- T-30m: Authorization check (approver confirms)
- T-5m: Observers start baseline recording (min 30s)
- T+0: Execute 60s pulsed signal
- T+0 → T+30m: Observation window (0–30s, 30s–5m, 5–30m recording segments)
- T+30m: Debrief and recommendation

Communications (conservative defaults — confirm)
- Primary channel: Secure Ops Channel (Radio 7). Confirm exact frequency/channel with Trial Lead.
- Primary comms contact (default): Ops Radio Lead (name TBD)
- Abort phrase: "ABORT TRIAL NOW" (repeat until acknowledged)

Safety Controls (non-negotiable)
- Hard stop: Safety Officer or Chief Negotiator can abort immediately for any escalation.
- Abort triggers: charging/aggressive approach, secondary Kaiju arrival, translator negative signal, human safety threat.
- Evacuation plan: predefined safe zones and routes for all personnel within 500 m of staging area.

Data & Evidence
- Observers must complete `method-02-observation-checklist.md` and attach timestamped video/audio/sensor logs.
- Translator must record verbatim signals and interpretations.
- Trial Lead to upload logs and a one-paragraph recommendation to coaching-state artifacts.

Decision Criteria
- Success: attention shift away from city ≥10 minutes, no escalation.
- Partial: brief or ambiguous shift — repeat with parameter tweaks.
- Fail: escalation or increased approach — stop further light trials.

Assumptions & Items to Confirm (action items)
1. Confirm primary comms channel and exact abort phrase (default: Secure Ops Channel / Radio 7; "ABORT TRIAL NOW").
2. Provide exact staging coordinates and verify 15 km clearance from populated areas (default: choose cleared staging area outside 15 km perimeter).
3. Confirm device operator and tower specs (default operator: Ops Lighting Team; conservative max brightness ≤50,000 lumens).
4. Set an exact test window datetime (default target: within 72 hours).
5. Confirm approver identity and that you will authorize at T-30m.
6. Confirm primary comms contact name/role (default: Ops Radio Lead).

Post-trial Actions
- If Success/Partial: schedule 2–3 follow-up trials to validate and parameterize the effect.
- If Fail: cease similar tests and escalate to containment planning and broader stakeholder consultation.

Saved to `.copilot-tracking/dt/negotiate-with-kaiju/method-02-trial-plan.md`. Marked assumptions require your confirmation before execution.
