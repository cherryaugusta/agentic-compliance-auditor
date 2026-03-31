import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_DIR = REPO_ROOT / "backend"
REPORTS_DIR = REPO_ROOT / "evals" / "reports"

sys.path.insert(0, str(BACKEND_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

import django  # noqa: E402

django.setup()

from apps.findings.models import ConflictFlag  # noqa: E402
from apps.findings.serializers import (  # noqa: E402
    EvidenceCitationSerializer,
    FindingMemoSerializer,
)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python ..\\infra\\scripts\\export_finding_packet.py <finding_id>")
        return 1

    try:
        finding_id = int(sys.argv[1])
    except ValueError:
        print("finding_id must be an integer.")
        return 1

    finding = ConflictFlag.objects.filter(id=finding_id).first()
    if finding is None:
        print(f"ConflictFlag not found for id={finding_id}")
        return 1

    packet = {
        "id": finding.id,
        "conflict_type": finding.conflict_type,
        "severity": finding.severity,
        "status": finding.status,
        "reason_summary": finding.reason_summary,
        "rules_triggered": finding.rules_triggered,
        "citations": EvidenceCitationSerializer(finding.citations.all(), many=True).data,
        "memo": FindingMemoSerializer(finding.memo).data if hasattr(finding, "memo") else None,
    }

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = REPORTS_DIR / f"export_finding_{finding.id}.json"
    output_path.write_text(json.dumps(packet, indent=2), encoding="utf-8")

    print(f"Wrote finding packet to: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
