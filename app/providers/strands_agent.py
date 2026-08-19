from __future__ import annotations


SYSTEM_PROMPT = """
You are PrizePilot for professionals and solo builders. Complete repetitive
application preparation end to end, surface only real decisions, and create an
audit trail. Never infer a missing eligibility fact and never submit externally
without a human approval record for that exact action.
""".strip()


def create_strands_agent():
    """Create the AWS Strands build used for Agents for Humans."""
    try:
        from strands import Agent
    except ImportError as exc:  # pragma: no cover - optional provider package
        raise RuntimeError("Install requirements.txt to use Strands Agents") from exc

    return Agent(system_prompt=SYSTEM_PROMPT)

