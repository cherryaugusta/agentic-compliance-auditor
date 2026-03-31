from rest_framework.response import Response
from rest_framework.views import APIView

from apps.comparisons.models import ComparisonRun
from apps.documents.models import PolicyDocument
from apps.evals.models import EvalRun
from apps.findings.models import ConflictFlag
from apps.reviews.models import ReviewTask


class MetricsOverviewView(APIView):
    def get(self, request):
        return Response(
            {
                "documents": PolicyDocument.objects.count(),
                "comparison_runs": ComparisonRun.objects.count(),
                "findings": ConflictFlag.objects.count(),
                "review_tasks": ReviewTask.objects.count(),
                "eval_runs": EvalRun.objects.count(),
            }
        )


class MetricsReviewOpsView(APIView):
    def get(self, request):
        return Response(
            {
                "unassigned": ReviewTask.objects.filter(
                    status=ReviewTask.Status.UNASSIGNED
                ).count(),
                "assigned": ReviewTask.objects.filter(status=ReviewTask.Status.ASSIGNED).count(),
                "in_review": ReviewTask.objects.filter(status=ReviewTask.Status.IN_REVIEW).count(),
                "approved": ReviewTask.objects.filter(status=ReviewTask.Status.APPROVED).count(),
                "dismissed": ReviewTask.objects.filter(status=ReviewTask.Status.DISMISSED).count(),
                "escalated": ReviewTask.objects.filter(status=ReviewTask.Status.ESCALATED).count(),
            }
        )


class MetricsConflictsView(APIView):
    def get(self, request):
        return Response(
            {
                "open": ConflictFlag.objects.filter(status=ConflictFlag.Status.OPEN).count(),
                "needs_review": ConflictFlag.objects.filter(
                    status=ConflictFlag.Status.NEEDS_REVIEW
                ).count(),
                "confirmed": ConflictFlag.objects.filter(
                    status=ConflictFlag.Status.CONFIRMED
                ).count(),
                "dismissed": ConflictFlag.objects.filter(
                    status=ConflictFlag.Status.DISMISSED
                ).count(),
                "escalated": ConflictFlag.objects.filter(
                    status=ConflictFlag.Status.ESCALATED
                ).count(),
                "resolved": ConflictFlag.objects.filter(
                    status=ConflictFlag.Status.RESOLVED
                ).count(),
                "degraded_runs": ComparisonRun.objects.filter(
                    status=ComparisonRun.Status.DEGRADED
                ).count(),
            }
        )
