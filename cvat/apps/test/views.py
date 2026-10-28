# Copyright (C) CVAT.ai Corporation
#
# SPDX-License-Identifier: MIT

from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cvat.apps.engine.models import Job
from cvat.apps.engine.types import ExtendedRequest
from cvat.utils import django_database as db_utils

from .permissions import TaskAnnotationCountsPermission
from .serializers import TaskAnnotationCountsSerializer
from .services import compute_annotation_counts


class TaskAnnotationCountsView(APIView):
    iam_permission_class = TaskAnnotationCountsPermission
    iam_supports_organization_params = True

    @extend_schema(
        tags=["test"],
        summary="Per-class annotation counts for a task",
        parameters=[
            OpenApiParameter(
                "task_id",
                OpenApiTypes.INT,
                OpenApiParameter.PATH,
                description="Task identifier",
            ),
            OpenApiParameter(
                "job_id",
                OpenApiTypes.INT,
                OpenApiParameter.QUERY,
                required=False,
                description="Optional job filter — only count annotations in this job",
            ),
        ],
        responses={200: TaskAnnotationCountsSerializer},
    )
    def get(self, request: ExtendedRequest, task_id: int) -> Response:
        job_id_raw = request.query_params.get("job_id")
        job_id = int(job_id_raw) if job_id_raw is not None else None

        if job_id is not None:
            db_utils.get_or_404(
                Job.objects.filter(segment__task_id=task_id),
                job_id,
            )

        counts = compute_annotation_counts(task_id=task_id, job_id=job_id)
        payload = {
            "task_id": task_id,
            "job_id": job_id,
            "counts": counts,
        }
        serializer = TaskAnnotationCountsSerializer(payload)
        return Response(serializer.data, status=status.HTTP_200_OK)
