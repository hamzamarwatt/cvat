# Copyright (C) CVAT.ai Corporation
#
# SPDX-License-Identifier: MIT

from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase

from cvat.apps.test.services import compute_annotation_counts


class AnnotationCountsServiceTest(SimpleTestCase):
    @patch("cvat.apps.test.services.LabeledTrack")
    @patch("cvat.apps.test.services.LabeledImage")
    @patch("cvat.apps.test.services.LabeledShape")
    def test_merges_counts_from_all_annotation_types(
        self, mock_shape, mock_image, mock_track
    ):
        def chain(model, rows):
            qs = MagicMock()
            qs.filter.return_value = qs
            qs.values.return_value = qs
            qs.annotate.return_value = rows
            model.objects = MagicMock()
            model.objects.filter.return_value = qs

        chain(mock_shape, [{"label__name": "cat", "count": 2}])
        chain(mock_image, [{"label__name": "cat", "count": 1}])
        chain(mock_track, [{"label__name": "dog", "count": 3}])

        result = {row["label"]: row["count"] for row in compute_annotation_counts(42)}

        self.assertEqual(result["cat"], 3)
        self.assertEqual(result["dog"], 3)
        mock_shape.objects.filter.assert_called_with(job__segment__task_id=42)

    @patch("cvat.apps.test.services.LabeledTrack")
    @patch("cvat.apps.test.services.LabeledImage")
    @patch("cvat.apps.test.services.LabeledShape")
    def test_job_id_filter_passed_to_query(self, mock_shape, mock_image, mock_track):
        for model in (mock_shape, mock_image, mock_track):
            qs = MagicMock()
            qs.filter.return_value = qs
            qs.values.return_value = qs
            qs.annotate.return_value = []
            model.objects = MagicMock()
            model.objects.filter.return_value = qs

        compute_annotation_counts(7, job_id=99)

        mock_shape.objects.filter.assert_called_with(job__segment__task_id=7, job_id=99)
