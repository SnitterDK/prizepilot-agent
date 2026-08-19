from __future__ import annotations

from typing import Iterable, List

from .models import (
    ActionState,
    ApplicantProfile,
    ApprovalItem,
    GateResult,
    GateState,
    Opportunity,
)


def evaluate_eligibility(
    profile: ApplicantProfile, opportunity: Opportunity
) -> GateResult:
    """Evaluate hard gates before an application draft is generated.

    Unknown evidence never becomes a positive claim. This is the central safety
    invariant: the agent may draft persuasively, but it cannot invent eligibility.
    """
    reasons: List[str] = []
    missing: List[str] = []

    excluded = {country.casefold() for country in opportunity.excluded_countries}
    if profile.country.casefold() in excluded:
        reasons.append(f"Residents of {profile.country} are excluded.")

    for attribute in opportunity.required_attributes:
        if not profile.attributes.get(attribute, False):
            reasons.append(f"Required attribute is not verified: {attribute}.")

    for evidence in opportunity.required_evidence:
        if not profile.evidence.get(evidence, "").strip():
            missing.append(evidence)

    if reasons:
        return GateResult(GateState.BLOCKED, reasons, missing)
    if missing:
        return GateResult(GateState.NEEDS_EVIDENCE, [], missing)
    return GateResult(GateState.PASS, [], [])


def build_approval_queue(
    profile: ApplicantProfile, opportunities: Iterable[Opportunity]
) -> List[ApprovalItem]:
    """Turn eligibility outcomes into a concise human approval queue."""
    queue: List[ApprovalItem] = []
    for opportunity in opportunities:
        result = evaluate_eligibility(profile, opportunity)
        if result.state is GateState.BLOCKED:
            queue.append(
                ApprovalItem(
                    opportunity=opportunity.name,
                    action="Do not apply",
                    destination=opportunity.organizer,
                    data_categories=[],
                    state=ActionState.BLOCKED,
                    rationale=" ".join(result.reasons),
                )
            )
        elif result.state is GateState.NEEDS_EVIDENCE:
            queue.append(
                ApprovalItem(
                    opportunity=opportunity.name,
                    action="Collect evidence",
                    destination=opportunity.organizer,
                    data_categories=result.missing_evidence,
                    state=ActionState.NEEDS_OWNER,
                    rationale="Missing: " + ", ".join(result.missing_evidence),
                )
            )
        else:
            queue.append(
                ApprovalItem(
                    opportunity=opportunity.name,
                    action="Review application draft",
                    destination=opportunity.organizer,
                    data_categories=["profile", "project", "application answers"],
                    state=ActionState.READY,
                    rationale="All configured hard gates passed.",
                )
            )
    return queue


def sample_opportunities() -> List[Opportunity]:
    return [
        Opportunity(
            name="All Things Agentic Hackathon",
            organizer="Google / Devpost",
            deadline="2026-08-31T17:00:00-07:00",
            prize="$180,000 cash",
            required_attributes=["internet_access"],
            required_evidence=["new_project_log", "repository", "demo_video"],
            required_stack=["Gemini 3.5", "Google ADK", "Google Cloud"],
        ),
        Opportunity(
            name="Agents for Humans Hackathon",
            organizer="AWS / Devpost",
            deadline="2026-09-14T17:00:00-07:00",
            prize="$40,000 cash",
            required_attributes=["internet_access"],
            required_evidence=["new_project_log", "public_repository", "demo_video"],
            required_stack=["Strands Agents SDK"],
        ),
        Opportunity(
            name="Student-only challenge",
            organizer="Example organizer",
            deadline="2026-09-30T00:00:00Z",
            prize="$10,000",
            required_attributes=["verified_student"],
        ),
    ]

