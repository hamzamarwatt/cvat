# Copyright (C) CVAT.ai Corporation
#
# SPDX-License-Identifier: MIT

from cvat.apps.engine.models import Task
from cvat.apps.engine.permissions import TaskPermission
from cvat.apps.engine.types import ExtendedRequest
from cvat.apps.iam.permissions import OpenPolicyAgentPermission, get_iam_context
from cvat.utils import django_database as db_utils


class TaskAnnotationCountsPermission(OpenPolicyAgentPermission):
    """Reuse task view permissions for read-only analytics."""

    @classmethod
    def create(cls, request: ExtendedRequest, view, obj, iam_context):
        task_id = view.kwargs.get("task_id")
        task = db_utils.get_or_404(Task.objects.select_related("project"), task_id)
        task_iam_context = get_iam_context(request, task)
        return [
            TaskPermission.create_base_perm(
                request,
                view,
                TaskPermission.Scopes.VIEW,
                task_iam_context,
                task,
            )
        ]

    @classmethod
    def _get_scopes(cls, request, view, obj):
        return []
