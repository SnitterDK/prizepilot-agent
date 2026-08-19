import unittest

from app.engine import build_approval_queue, evaluate_eligibility
from app.models import ApplicantProfile, GateState, Opportunity


class EligibilityTests(unittest.TestCase):
    def setUp(self):
        self.profile = ApplicantProfile(
            country="Denmark",
            is_adult=True,
            works_solo=True,
            attributes={"internet_access": True, "verified_student": False},
            evidence={"repository": "https://example.test/repo"},
        )

    def test_blocks_unverified_hard_attribute(self):
        opportunity = Opportunity(
            name="Student challenge",
            organizer="Example",
            deadline="2026-09-01",
            prize="$1",
            required_attributes=["verified_student"],
        )
        result = evaluate_eligibility(self.profile, opportunity)
        self.assertEqual(result.state, GateState.BLOCKED)

    def test_surfaces_missing_evidence_without_inventing_it(self):
        opportunity = Opportunity(
            name="Agent challenge",
            organizer="Example",
            deadline="2026-09-01",
            prize="$1",
            required_attributes=["internet_access"],
            required_evidence=["repository", "demo_video"],
        )
        result = evaluate_eligibility(self.profile, opportunity)
        self.assertEqual(result.state, GateState.NEEDS_EVIDENCE)
        self.assertEqual(result.missing_evidence, ["demo_video"])

    def test_queue_marks_safe_block(self):
        opportunity = Opportunity(
            name="Student challenge",
            organizer="Example",
            deadline="2026-09-01",
            prize="$1",
            required_attributes=["verified_student"],
        )
        item = build_approval_queue(self.profile, [opportunity])[0]
        self.assertEqual(item.state.value, "blocked")
        self.assertEqual(item.action, "Do not apply")


if __name__ == "__main__":
    unittest.main()

