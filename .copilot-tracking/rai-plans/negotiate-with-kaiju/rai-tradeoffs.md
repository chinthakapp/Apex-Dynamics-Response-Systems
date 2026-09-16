# Phase 5 — RAI Tradeoffs

Purpose: Document key tradeoffs between trustworthiness characteristics encountered during impact assessment.

1. Safety vs Privacy
- Issue: Detailed telemetry and sensor feeds improve safety evaluation but risk exposing PII and sensitive locations.
- Mitigation: Tiered access controls, redaction at ingest, and differential access for investigators.

2. Transparency vs Security
- Issue: Detailed logs and explainability artifacts aid audits but may reveal model internals that help adversaries.
- Mitigation: Provide summary-level explanations for external audits, full technical logs only under secure access with justification.

3. Responsiveness vs Robustness
- Issue: Low-latency edge actuation favors quick decisions but reduces time for cross-checks and human approvals.
- Mitigation: Hybrid approach — allow automated safe-mode actions locally, escalate high-impact actions for two-person approval.

4. Explainability vs Model Performance
- Issue: Constraining models for interpretability can reduce raw performance on novel inputs.
- Mitigation: Use ensemble models with separate interpretable surrogate models for explanations.

5. Usability vs Restriction
- Issue: Strict rate-limiting and truncation reduce model abuse but can impede legitimate high-throughput use.
- Mitigation: Adaptive throttling with whitelisted operator roles and burst allowances under monitoring.

6. Evidence Collection vs Operational Overhead
- Issue: Aggressive logging and immutable storage increase costs and latency.
- Mitigation: Policy-driven retention tiers, sampling for routine telemetry, full capture for incidents.

Recommendations: Adopt a default "safety-first" posture for life-safety actions, require two-person approval for any actuation that affects humans or infrastructure, and keep comprehensive evidence capture for incident investigation with strict RBAC.
