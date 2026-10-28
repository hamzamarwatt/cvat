# Copyright (C) CVAT.ai Corporation
#
# SPDX-License-Identifier: MIT

from django.urls import path

from . import views

urlpatterns = [
    path(
        "tasks/<int:task_id>/annotation-counts",
        views.TaskAnnotationCountsView.as_view(),
        name="task_annotation_counts",
    ),
]
