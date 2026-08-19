from __future__ import annotations

import os


SYSTEM_INSTRUCTION = """
You are PrizePilot, an autonomous application preparation agent. Find the next
useful action, but never invent eligibility, traction, partnerships, education,
revenue, or measured impact. Stop at external transmission and final submission
until the human has approved the exact destination, data, and claims. Return a
short audit note for every decision.
""".strip()


def create_google_agent():
    """Create the Google ADK build used for the Google Cloud submission."""
    try:
        from google.adk.agents import Agent
    except ImportError as exc:  # pragma: no cover - optional provider package
        raise RuntimeError("Install requirements.txt to use Google ADK") from exc

    return Agent(
        name="prizepilot_google",
        model=os.getenv("GEMINI_MODEL", "gemini-3.5-flash"),
        description="Auditable opportunity triage and application preparation",
        instruction=SYSTEM_INSTRUCTION,
    )

