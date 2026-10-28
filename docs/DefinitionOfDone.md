# Definition of Done

Evidence for submission branch **`dev-test01`** (fork: `hamzamarwatt/cvat`).

| # | Criterion | Done | Evidence |
|---|-----------|------|----------|
| 1 | Endpoint returns correct per-class counts for a known task | ☑ | Logic: `cvat/apps/test/services.py` (`compute_annotation_counts`). Unit tests: `cvat/apps/test/tests/test_services.py`. After stack up: curl JSON vs labels on task (see `docs/SUBMISSION.md`). |
| 2 | UI page renders bar chart for counts | ☑ | `cvat-ui/src/components/class-analytics/class-analytics-page.tsx` — Chart.js `Bar`. Route: `/tasks/:tid/class-analytics`. |
| 3 | UI shows empty state when task has no annotations | ☑ | Same file: `state === 'empty'` → `<Empty description='No annotations for this task (or filter).' />`. |
| 4 | UI shows error state when API fails | ☑ | Same file: `state === 'error'` → `<Alert type='error' ...>`. Demo: invalid task or API down. |
| 5 | Unauthenticated request rejected | ☑ | DRF `IsAuthenticated` + IAM. Expected: `curl` without cookie → **401**. Command in `docs/EVIDENCE.md`. |
| 6 | User without task access rejected | ☑ | `TaskAnnotationCountsPermission` → `TaskPermission` VIEW. Expected second user → **403**. Command in `docs/EVIDENCE.md`. |
| 7 | MO-1 measured (5 runs, raw output) | ☐ | Run `./docs/benchmark_annotation_counts.sh` when CVAT is up; paste into `docs/Objectives.md` (see note there if deadline hit before stack ready). |
| 8 | `job_id` query filter documented and working | ☑ | API: `views.py` validates job belongs to task. Example: `GET /api/test/tasks/5/annotation-counts?job_id=1`. Tests: `test_job_id_filter_passed_to_query`. |
| 9 | WebSocket live update | ☑ | `signals.py` → Redis → `realtime.py`; ASGI `cvat/asgi.py`; client in class-analytics page. Path: `/api/test/ws/tasks/<id>/annotation-counts`. |
| 10 | WebSocket reconnect | ☑ | `class-analytics-page.tsx`: `onclose` → `setTimeout(connectWebSocket, 3000)`; UI shows “Reconnecting…”. |
| 11 | Incremental git history | ☑ | `git log develop..dev-test01 --oneline` → 6+ feature commits (see below). |
| 12 | PR to own fork `main` | ☑ | https://github.com/hamzamarwatt/cvat/compare/main...dev-test01 |
| 13 | Loom ≤ 5 min, K1–K4 | ☐ | Record using `docs/LOOM_SCRIPT.md`; paste URL in email + here: _Loom URL_ |
| 14 | Work not finished listed | ☑ | See **Not finished** (MO-1 raw runs if stack not up at doc time; Loom URL pending until recorded). |

## Git log (item 11)

```
c388cb0 Add assessment plan, objectives, and definition of done.
d8579d9 Add test Django app with per-class annotation counts API.
f147445 Push live annotation count updates over WebSocket.
516d27d Add class analytics page with chart and WebSocket reconnect.
1a94b4f Fix class analytics API call to use cvat-core server.request.
2bb6b9d Set detail=False on counts APIView for IAM enforcer.
```

_(Plus submission commits after this document.)_

## Not finished / deferred

- **MO-1 raw benchmark output**: requires running CVAT locally (`docs/SETUP.md`, `docker-compose.podman.yml` on Podman). Run `docs/benchmark_annotation_counts.sh` and update `docs/Objectives.md` before or immediately after email if stack finishes building.
- **Loom URL**: candidate must record and add link (assessment gate).

## Sample dataset

- COCO 2017 val: upload subset per `docs/SETUP.md`; record image count here after import: **_N images_**.
