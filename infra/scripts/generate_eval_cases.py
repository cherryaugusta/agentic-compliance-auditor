import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DATASET_ROOT = REPO_ROOT / "evals" / "datasets"

SCENARIOS = [
    ("contradiction_cases", "direct_contradiction", "timeline_conflict", "high"),
    ("drift_cases", "version_drift", "coverage_gap", "medium"),
    ("stale_reference_cases", "stale_reference", "stale_reference", "medium"),
    ("no_conflict_cases", "no_conflict", None, None),
    ("adversarial_cases", "adversarial_wording", "terminology_drift", "medium"),
    ("fallback_cases", "provider_failure", None, None),
]


def build_documents(case_id: str, scenario_type: str) -> list[dict]:
    if scenario_type == "direct_contradiction":
        return [
            {
                "document_type": "internal_policy",
                "title": f"{case_id} Source",
                "version_label": "v1",
                "effective_date": "2026-01-15",
                "text": "Escalated complaints must be acknowledged within 10 business days.",
            },
            {
                "document_type": "control_library",
                "title": f"{case_id} Target",
                "version_label": "v2",
                "effective_date": "2026-02-01",
                "text": "Escalated complaints must be acknowledged within 5 business days.",
            },
        ]

    if scenario_type == "version_drift":
        return [
            {
                "document_type": "internal_policy",
                "title": f"{case_id} Source",
                "version_label": "v3",
                "effective_date": "2026-01-15",
                "text": (
                    "Complaints triage must include vulnerability flags " "and callback evidence."
                ),
            },
            {
                "document_type": "control_library",
                "title": f"{case_id} Target",
                "version_label": "v4",
                "effective_date": "2026-02-01",
                "text": "Complaints triage must include callback evidence.",
            },
        ]

    if scenario_type == "stale_reference":
        return [
            {
                "document_type": "procedure",
                "title": f"{case_id} Source",
                "version_label": "v2",
                "effective_date": "2025-10-01",
                "text": "Use control library v2 for complaints routing.",
            },
            {
                "document_type": "control_library",
                "title": f"{case_id} Target",
                "version_label": "v5",
                "effective_date": "2026-02-01",
                "text": "Complaints Control Standard v5 is the active control baseline.",
            },
        ]

    if scenario_type == "no_conflict":
        return [
            {
                "document_type": "internal_policy",
                "title": f"{case_id} Source",
                "version_label": "v1",
                "effective_date": "2026-01-15",
                "text": "Escalated complaints must be acknowledged within 5 business days.",
            },
            {
                "document_type": "control_library",
                "title": f"{case_id} Target",
                "version_label": "v2",
                "effective_date": "2026-02-01",
                "text": "Escalated complaints must be acknowledged within 5 business days.",
            },
        ]

    if scenario_type == "adversarial_wording":
        return [
            {
                "document_type": "internal_policy",
                "title": f"{case_id} Source",
                "version_label": "v1",
                "effective_date": "2026-01-15",
                "text": "Escalated complaints must be acknowledged promptly after intake review.",
            },
            {
                "document_type": "control_library",
                "title": f"{case_id} Target",
                "version_label": "v2",
                "effective_date": "2026-02-01",
                "text": (
                    "Escalated complaints require immediate acknowledgment "
                    "following case triage."
                ),
            },
        ]

    if scenario_type == "provider_failure":
        return [
            {
                "document_type": "internal_policy",
                "title": f"{case_id} Source",
                "version_label": "v1",
                "effective_date": "2026-01-15",
                "text": "Complaint acknowledgments must be recorded in the case file.",
            },
            {
                "document_type": "control_library",
                "title": f"{case_id} Target",
                "version_label": "v2",
                "effective_date": "2026-02-01",
                "text": "Complaint acknowledgments must be recorded in the case file.",
            },
        ]

    raise ValueError(f"Unsupported scenario_type: {scenario_type}")


def build_expected_statements(scenario_type: str) -> list[dict]:
    if scenario_type == "direct_contradiction":
        return [
            {
                "statement_type": "timeline",
                "normalized_text_contains": "acknowledged within",
            }
        ]
    if scenario_type == "stale_reference":
        return [
            {
                "statement_type": "control",
                "normalized_text_contains": "control library v2",
            }
        ]
    if scenario_type == "adversarial_wording":
        return [
            {
                "statement_type": "control",
                "normalized_text_contains": "acknowledged",
            }
        ]
    return [
        {
            "statement_type": "control",
            "normalized_text_contains": "",
        }
    ]


def payload(
    case_id: str,
    scenario_type: str,
    expected_conflict_type: str | None,
    expected_severity: str | None,
) -> dict:
    return {
        "case_id": case_id,
        "scenario_type": scenario_type,
        "documents": build_documents(case_id, scenario_type),
        "expected_statements": build_expected_statements(scenario_type),
        "expected_conflict_type": expected_conflict_type,
        "expected_severity": expected_severity,
        "expected_requires_review": True if expected_conflict_type else False,
        "expected_citation_targets": [
            {"title": f"{case_id} Source"},
            {"title": f"{case_id} Target"},
        ],
    }


def main() -> None:
    total = 0
    for folder, scenario_type, conflict_type, severity in SCENARIOS:
        target = DATASET_ROOT / folder
        target.mkdir(parents=True, exist_ok=True)
        for index in range(1, 9):
            total += 1
            case_id = f"eval-{scenario_type}-{index:03d}"
            case_path = target / f"{case_id}.json"
            with case_path.open("w", encoding="utf-8") as handle:
                json.dump(
                    payload(case_id, scenario_type, conflict_type, severity),
                    handle,
                    indent=2,
                )
    print(f"Generated {total} eval cases.")


if __name__ == "__main__":
    main()
