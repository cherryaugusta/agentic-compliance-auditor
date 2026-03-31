from celery import shared_task

from .models import ComparisonRun
from .services import compare_run


@shared_task
def run_comparison(run_id: int) -> None:
    run = ComparisonRun.objects.get(id=run_id)
    compare_run(run)
