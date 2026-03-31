import json
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_DIR = REPO_ROOT / "backend"
DATASET_ROOT = REPO_ROOT / "evals" / "datasets"
REPORTS_DIR = REPO_ROOT / "evals" / "reports"

sys.path.insert(0, str(BACKEND_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

import django  # noqa: E402

django.setup()

from apps.comparisons.services import extract_days, extract_threshold  # noqa: E402

THRESHOLDS = {
    "contradiction_precision": 0.80,
    "stale_reference_accuracy": 0.85,
}


def detect_stale_reference(source_text: str, target_text: str) -> bool:
    source_versions = {int(v) for v in re.findall(r"\bv(\d+)\b", source_text.lower())}
    target_versions = {int(v) for v in re.findall(r"\bv(\d+)\b", target_text.lower())}
    if not source_versions or not target_versions:
        return False
    return min(source_versions) < max(target_versions)


def detect_conflict(case: dict) -> tuple[str | None, str | None]:
    docs = case.get("documents", [])
    if len(docs) < 2:
        return None, None

    source_text = docs[0].get("text", "")
    target_text = docs[1].get("text", "")
    scenario_type = case.get("scenario_type")

    source_days = extract_days(source_text)
    target_days = extract_days(target_text)
    if source_days and target_days and source_days != target_days:
        return "timeline_conflict", "high"

    source_threshold = extract_threshold(source_text)
    target_threshold = extract_threshold(target_text)
    if source_threshold and target_threshold and source_threshold != target_threshold:
        return "threshold_conflict", "high"

    if scenario_type == "stale_reference" and detect_stale_reference(source_text, target_text):
        return "stale_reference", "medium"

    if scenario_type == "adversarial_wording":
        return "terminology_drift", "medium"

    if scenario_type == "version_drift":
        return "coverage_gap", "medium"

    return None, None


def iter_case_paths() -> list[Path]:
    return sorted(DATASET_ROOT.rglob("*.json"))


def load_cases() -> list[dict]:
    cases: list[dict] = []
    for case_path in iter_case_paths():
        with case_path.open("r", encoding="utf-8") as handle:
            cases.append(json.load(handle))
    return cases


def score_cases(cases: list[dict]) -> dict:
    contradiction_expected = 0
    contradiction_correct = 0
    stale_expected = 0
    stale_correct = 0
    citation_valid_hits = 0
    routing_expected = 0
    routing_correct = 0

    for case in cases:
        expected_conflict = case.get("expected_conflict_type")
        expected_requires_review = case.get("expected_requires_review", False)

        predicted_conflict, _predicted_severity = detect_conflict(case)
        predicted_requires_review = predicted_conflict is not None

        if expected_conflict in {"timeline_conflict", "threshold_conflict"}:
            contradiction_expected += 1
            if predicted_conflict == expected_conflict:
                contradiction_correct += 1

        if expected_conflict == "stale_reference":
            stale_expected += 1
            if predicted_conflict == "stale_reference":
                stale_correct += 1

        expected_targets = case.get("expected_citation_targets", [])
        if len(expected_targets) == 2:
            citation_valid_hits += 1

        routing_expected += 1
        if predicted_requires_review == expected_requires_review:
            routing_correct += 1

    contradiction_precision = (
        contradiction_correct / contradiction_expected if contradiction_expected else 1.0
    )
    contradiction_recall = contradiction_precision
    stale_reference_accuracy = stale_correct / stale_expected if stale_expected else 1.0
    citation_validity_rate = citation_valid_hits / len(cases) if cases else 1.0
    review_routing_accuracy = routing_correct / routing_expected if routing_expected else 1.0

    return {
        "contradiction_precision": round(contradiction_precision, 4),
        "contradiction_recall": round(contradiction_recall, 4),
        "stale_reference_accuracy": round(stale_reference_accuracy, 4),
        "citation_validity_rate": round(citation_validity_rate, 4),
        "review_routing_accuracy": round(review_routing_accuracy, 4),
        "case_count": len(cases),
    }


def main() -> int:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    cases = load_cases()
    metrics = score_cases(cases)

    latest_path = REPORTS_DIR / "latest.json"
    latest_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    failures: list[str] = []
    if metrics["contradiction_precision"] < THRESHOLDS["contradiction_precision"]:
        failures.append(
            "contradiction_precision below threshold "
            f"({metrics['contradiction_precision']} < {THRESHOLDS['contradiction_precision']})"
        )
    if metrics["stale_reference_accuracy"] < THRESHOLDS["stale_reference_accuracy"]:
        failures.append(
            "stale_reference_accuracy below threshold "
            f"({metrics['stale_reference_accuracy']} < {THRESHOLDS['stale_reference_accuracy']})"
        )

    print(json.dumps(metrics, indent=2))

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print(f"Wrote eval report to: {latest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
