from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List


class GateState(str, Enum):
    PASS = "pass"
    NEEDS_EVIDENCE = "needs_evidence"
    BLOCKED = "blocked"


class ActionState(str, Enum):
    READY = "ready"
    NEEDS_OWNER = "needs_owner"
    BLOCKED = "blocked"
    APPROVED = "approved"


@dataclass(frozen=True)
class ApplicantProfile:
    country: str
    is_adult: bool
    works_solo: bool
    attributes: Dict[str, bool] = field(default_factory=dict)
    evidence: Dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class Opportunity:
    name: str
    organizer: str
    deadline: str
    prize: str
    required_attributes: List[str] = field(default_factory=list)
    required_evidence: List[str] = field(default_factory=list)
    excluded_countries: List[str] = field(default_factory=list)
    required_stack: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class GateResult:
    state: GateState
    reasons: List[str]
    missing_evidence: List[str]


@dataclass
class ApprovalItem:
    opportunity: str
    action: str
    destination: str
    data_categories: List[str]
    state: ActionState
    rationale: str
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

