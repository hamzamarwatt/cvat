# Copyright (C) CVAT.ai Corporation
#
# SPDX-License-Identifier: MIT

from rest_framework import serializers


class LabelCountSerializer(serializers.Serializer):
    label = serializers.CharField()
    count = serializers.IntegerField(min_value=0)


class TaskAnnotationCountsSerializer(serializers.Serializer):
    task_id = serializers.IntegerField()
    job_id = serializers.IntegerField(required=False, allow_null=True)
    counts = LabelCountSerializer(many=True)
