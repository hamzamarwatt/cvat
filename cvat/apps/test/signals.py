# Copyright (C) CVAT.ai Corporation
#
# SPDX-License-Identifier: MIT

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from cvat.apps.engine.models import Job, LabeledImage, LabeledShape, LabeledTrack

from .realtime import broadcast_task_counts


def _task_id_for_job(job_id: int) -> int | None:
    try:
        return Job.objects.values_list("segment__task_id", flat=True).get(pk=job_id)
    except Job.DoesNotExist:
        return None


def _notify_job(job_id: int) -> None:
    task_id = _task_id_for_job(job_id)
    if task_id is not None:
        broadcast_task_counts(task_id)


@receiver(post_save, sender=LabeledShape)
@receiver(post_delete, sender=LabeledShape)
@receiver(post_save, sender=LabeledImage)
@receiver(post_delete, sender=LabeledImage)
@receiver(post_save, sender=LabeledTrack)
@receiver(post_delete, sender=LabeledTrack)
def annotation_changed(sender, instance, **kwargs):
    _notify_job(instance.job_id)
