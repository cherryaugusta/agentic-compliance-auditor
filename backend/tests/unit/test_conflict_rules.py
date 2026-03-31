from apps.comparisons.services import extract_days, extract_threshold, score_severity
from apps.findings.models import ConflictFlag


def test_extract_days_returns_integer_for_business_days():
    assert extract_days("Escalated complaints must be acknowledged within 10 business days.") == 10


def test_extract_days_returns_integer_for_days():
    assert extract_days("The team must respond within 5 days.") == 5


def test_extract_days_returns_none_when_no_timeline_present():
    assert extract_days("The team must respond promptly.") is None


def test_extract_threshold_returns_integer():
    assert extract_threshold("Approval is required for amounts above £1,500.") == 1500


def test_extract_threshold_returns_none_when_no_threshold_present():
    assert extract_threshold("Approval is required for exceptional cases.") is None


def test_score_severity_is_high_for_timeline_conflict():
    severity = score_severity(ConflictFlag.ConflictType.TIMELINE_CONFLICT, 10, 5)
    assert severity == ConflictFlag.Severity.HIGH


def test_score_severity_is_high_for_threshold_conflict():
    severity = score_severity(ConflictFlag.ConflictType.THRESHOLD_CONFLICT, 1500, 1000)
    assert severity == ConflictFlag.Severity.HIGH


def test_score_severity_is_medium_for_stale_reference():
    severity = score_severity(ConflictFlag.ConflictType.STALE_REFERENCE, None, None)
    assert severity == ConflictFlag.Severity.MEDIUM
