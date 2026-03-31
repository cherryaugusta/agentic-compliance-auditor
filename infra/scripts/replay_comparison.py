import os
import sys
import uuid
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_DIR = REPO_ROOT / "backend"
sys.path.insert(0, str(BACKEND_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

import django  # noqa: E402

django.setup()

from apps.comparisons.models import ComparisonRun  # noqa: E402
from apps.comparisons.tasks import run_comparison  # noqa: E402


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python ..\\infra\\scripts\\replay_comparison.py <run_id>")
        return 1

    try:
        run_id = int(sys.argv[1])
    except ValueError:
        print("run_id must be an integer.")
        return 1

    original = ComparisonRun.objects.filter(id=run_id).first()
    if original is None:
        print(f"ComparisonRun not found for id={run_id}")
        return 1

    replay = ComparisonRun.objects.create(
        source_document=original.source_document,
        run_type=original.run_type,
        target_document_ids=original.target_document_ids,
        config_snapshot={
            **original.config_snapshot,
            "replayed_from_run_id": original.id,
        },
        status=ComparisonRun.Status.PENDING,
        correlation_id=str(uuid.uuid4()),
    )
    run_comparison(replay.id)

    print(f"Replayed run created with id={replay.id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
