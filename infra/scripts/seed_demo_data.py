import hashlib
import os
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_DIR = REPO_ROOT / "backend"
sys.path.insert(0, str(BACKEND_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

import django  # noqa: E402

django.setup()

from apps.comparisons.models import ComparisonRun  # noqa: E402
from apps.comparisons.tasks import run_comparison  # noqa: E402
from apps.documents.models import PolicyDocument  # noqa: E402
from apps.documents.tasks import parse_and_extract_document  # noqa: E402
from apps.evals.models import EvalRun  # noqa: E402
from apps.lineage.models import DocumentLineage  # noqa: E402
from apps.observability.models import PromptVersion  # noqa: E402
from django.contrib.auth import get_user_model  # noqa: E402


def checksum(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def upsert_user(username: str, is_superuser: bool = False) -> None:
    user_model = get_user_model()
    user, created = user_model.objects.get_or_create(
        username=username,
        defaults={
            "email": f"{username}@local.test",
            "is_staff": True,
            "is_superuser": is_superuser,
        },
    )
    if created:
        user.set_password("Password123!")
        user.save(update_fields=["password"])

    changed = False
    if user.email != f"{username}@local.test":
        user.email = f"{username}@local.test"
        changed = True
    if user.is_staff is not True:
        user.is_staff = True
        changed = True
    if user.is_superuser != is_superuser:
        user.is_superuser = is_superuser
        changed = True
    if changed:
        user.save(update_fields=["email", "is_staff", "is_superuser"])


def upsert_doc(**kwargs) -> PolicyDocument:
    document, _ = PolicyDocument.objects.update_or_create(
        title=kwargs["title"],
        version_label=kwargs["version_label"],
        defaults=kwargs,
    )
    return document


def seed_documents() -> list[PolicyDocument]:
    documents: list[PolicyDocument] = []

    documents.append(
        upsert_doc(
            document_type="internal_policy",
            title="Complaints Escalation Policy v3",
            source_name="Internal Policy Office",
            domain_area="complaints",
            owner_team="Compliance",
            version_label="v3",
            effective_date=date(2026, 1, 15),
            is_external_source=False,
            status="active",
            storage_path="demo_data/internal_policies/complaints_escalation_policy_v3.txt",
            sha256_checksum=checksum(
                "Escalated complaints must be acknowledged within 10 business days."
            ),
            content_text="Escalated complaints must be acknowledged within 10 business days.",
        )
    )
    documents.append(
        upsert_doc(
            document_type="control_library",
            title="Complaints Control Standard",
            source_name="Internal Standards Board",
            domain_area="complaints",
            owner_team="Risk",
            version_label="v5",
            effective_date=date(2026, 2, 1),
            is_external_source=False,
            status="active",
            storage_path="demo_data/control_libraries/complaints_control_standard_v5.txt",
            sha256_checksum=checksum(
                "Escalated complaints must be acknowledged within 5 business days."
            ),
            content_text="Escalated complaints must be acknowledged within 5 business days.",
        )
    )
    documents.append(
        upsert_doc(
            document_type="procedure",
            title="Complaints Procedure v2",
            source_name="Operations",
            domain_area="complaints",
            owner_team="Operations",
            version_label="v2",
            effective_date=date(2025, 10, 1),
            is_external_source=False,
            status="active",
            storage_path="demo_data/procedures/complaints_procedure_v2.txt",
            sha256_checksum=checksum("Use control library v2 for complaints routing."),
            content_text="Use control library v2 for complaints routing.",
        )
    )
    documents.append(
        upsert_doc(
            document_type="guidance",
            title="Vulnerable Customer Guidance 2026",
            source_name="External Regulator",
            domain_area="vulnerable_customers",
            owner_team="Compliance",
            version_label="2026.1",
            effective_date=date(2026, 2, 15),
            is_external_source=True,
            status="active",
            storage_path="demo_data/external_guidance/vulnerable_customer_guidance_2026.txt",
            sha256_checksum=checksum(
                "Vulnerable-customer escalations must be reviewed proactively."
            ),
            content_text="Vulnerable-customer escalations must be reviewed proactively.",
        )
    )

    for idx in range(5, 13):
        documents.append(
            upsert_doc(
                document_type="internal_policy",
                title=f"Seeded Demo Policy {idx}",
                source_name="Seed Generator",
                domain_area="other",
                owner_team="Governance",
                version_label="v1",
                effective_date=date(2026, 1, min(idx, 28)),
                is_external_source=False,
                status="active",
                storage_path=f"demo_data/internal_policies/seeded_demo_policy_{idx}.txt",
                sha256_checksum=checksum(f"Seeded policy body {idx}."),
                content_text=f"Seeded policy body {idx}.",
            )
        )

    return documents


def seed_lineage() -> None:
    source = PolicyDocument.objects.get(
        title="Complaints Escalation Policy v3",
        version_label="v3",
    )
    target = PolicyDocument.objects.get(
        title="Complaints Control Standard",
        version_label="v5",
    )
    DocumentLineage.objects.get_or_create(
        parent_document=source,
        child_document=target,
        relationship_type="aligned_to",
    )


def seed_prompts() -> None:
    prompts = [
        ("sectioning-default", "v1", "sectioning", "Split policy text into clean sections."),
        (
            "statement-extraction-default",
            "v1",
            "statement_extraction",
            "Extract control statements.",
        ),
        (
            "contradiction-analysis-default",
            "v1",
            "contradiction_analysis",
            "Draft contradiction rationale.",
        ),
        ("memo-generation-default", "v1", "memo_generation", "Draft finding memo."),
    ]
    for name, version_label, purpose, template_text in prompts:
        PromptVersion.objects.update_or_create(
            name=name,
            version_label=version_label,
            defaults={
                "purpose": purpose,
                "template_text": template_text,
                "schema_version": "v1",
                "is_active": True,
            },
        )


def run_parsing() -> None:
    for doc in PolicyDocument.objects.all().order_by("id"):
        parse_and_extract_document(doc.id)


def seed_comparison() -> None:
    source = PolicyDocument.objects.get(
        title="Complaints Escalation Policy v3",
        version_label="v3",
    )
    target = PolicyDocument.objects.get(
        title="Complaints Control Standard",
        version_label="v5",
    )

    ComparisonRun.objects.filter(correlation_id="seeded-run-001").delete()

    run = ComparisonRun.objects.create(
        source_document=source,
        run_type="policy_vs_control",
        target_document_ids=[target.id],
        config_snapshot={"seeded": True},
        status="pending",
        correlation_id="seeded-run-001",
    )
    run_comparison(run.id)


def seed_eval_baseline() -> None:
    EvalRun.objects.update_or_create(
        run_label="baseline-seeded",
        defaults={
            "status": "completed",
            "config_snapshot": {"mode": "rules+mock"},
            "summary_metrics": {
                "contradiction_precision": 0.89,
                "contradiction_recall": 0.86,
                "stale_reference_accuracy": 0.93,
                "citation_validity_rate": 1.0,
                "review_routing_accuracy": 0.91,
            },
        },
    )


def main() -> None:
    upsert_user("admin", is_superuser=True)
    upsert_user("reviewer1")
    upsert_user("reviewer2")

    seed_documents()
    seed_lineage()
    seed_prompts()
    run_parsing()
    seed_comparison()
    seed_eval_baseline()

    print("Seed complete.")


if __name__ == "__main__":
    main()
