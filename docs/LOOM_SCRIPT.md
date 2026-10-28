# Loom script (≤ 5 minutes)

Record your screen + face. Do **not** read this verbatim — use it as a guide. Answers must match **your** repo.

## 0:00–1:00 — Demo

1. Open http://localhost:8080 (or explain if stack was still building: show PR + code path).
2. Log in → open a task with COCO annotations.
3. **Tasks → ⋮ → Class analytics** or `/tasks/<id>/class-analytics`.
4. Show bar chart, optional **job ID** filter, **empty** task if you have one.
5. Briefly show **Reconnecting…** after disabling network or restarting Redis (optional).

## 1:00–2:30 — Code path (one request)

1. UI: `cvat-ui/src/components/class-analytics/class-analytics-page.tsx` — `core.server.request` to `/api/test/tasks/.../annotation-counts`.
2. URL routing: `cvat/urls.py` → `cvat/apps/test/urls.py`.
3. View: `cvat/apps/test/views.py` — `TaskAnnotationCountsView`.
4. Count logic: `cvat/apps/test/services.py` — `compute_annotation_counts`.
5. Auth: `cvat/apps/test/permissions.py` — delegates to `TaskPermission` VIEW on the task.

## 2:30–5:00 — Four questions (out loud)

**K1 — Which file and line computes the per-class count, and why there?**  
`cvat/apps/test/services.py`, function `compute_annotation_counts`. It aggregates ORM counts for shapes, images, and tracks by `label__name` for all jobs in the task. Kept out of the view so the query stays testable and the view stays thin; tests in `cvat/apps/test/tests/test_services.py`.

**K2 — Where is the label stored; model and field; task → label name?**  
Model **`Label`**, field **`name`** (`cvat/apps/engine/models.py`). Annotations (`LabeledShape` / `LabeledImage` / `LabeledTrack`) have **`label`** FK → `Label`. Task → **`Segment`** → **`Job`** → annotation rows → **`label.name`**.

**K3 — One thing you would reverse and the cost?**  
Example: WebSocket auth via session cookie parsing in `websocket.py` instead of reusing DRF middleware — cost: re-test auth edge cases and maintain ASGI glue; benefit: simpler permission reuse via `TaskAnnotationCountsPermission` pattern.

**K4 — One thing you did not understand and what you did?**  
Example: CVAT IAM / OPA on first read — traced `PolicyEnforcer` and `TaskPermission.create_base_perm`, set `detail=False` on `APIView` after hitting permission checks; read consensus app for the same pattern.
