# Copyright (C) CVAT.ai Corporation
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

from collections import defaultdict
from typing import TypedDict

from django.db.models import Count

from cvat.apps.engine.models import LabeledImage, LabeledShape, LabeledTrack


class LabelCount(TypedDict):
    label: str
    count: int


def compute_annotation_counts(task_id: int, job_id: int | None = None) -> list[LabelCount]:
    """
    Count annotations per label name for all jobs in a task.

    Shapes, image tags, and tracks are merged into one count per class name.
    """
    job_filter: dict = {"job__segment__task_id": task_id}
    if job_id is not None:
        job_filter["job_id"] = job_id

    totals: dict[str, int] = defaultdict(int)

    for model in (LabeledShape, LabeledImage, LabeledTrack):
        rows = (
            model.objects.filter(**job_filter)
            .values("label__name")
            .annotate(count=Count("id"))
        )
        for row in rows:
            totals[row["label__name"]] += row["count"]

    return [{"label": name, "count": count} for name, count in sorted(totals.items())]
