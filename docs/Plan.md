# Plan — Annotation Analytics (xis.ai assessment)

**Acknowledged:** 28 Oct 2026, 17:57 (UTC+5)  
**CVAT commit (clone):** `a81ed252dce15b805d5a544116cf98005e42f257`  
**Branch:** `dev-test01`

## Goal

Add per-class annotation counts for a CVAT task: REST API (Django app `test`), UI page with bar chart, auth via existing CVAT IAM, one measured performance objective, optional `job_id` filter, then live updates over WebSocket if time allows.

## Time budget (8 h)

| Block | Duration | Work |
|-------|----------|------|
| 0 | 0:00–0:30 | Fork/clone, Docker + COCO import (not counted per brief) |
| 1 | 0:30–1:00 | This plan + Objectives + Definition of Done → **first commit** |
| 2 | 1:00–3:00 | Explore engine models; `test` app + counts API |
| 3 | 3:00–4:30 | UI route, Chart.js graph, empty + error states |
| 4 | 4:30–5:30 | Auth demos; benchmark script; `job_id` filter |
| 5 | 5:30–7:00 | WebSocket broadcast + UI reconnect (only after 1–4 done) |
| 6 | 7:00–8:00 | Final docs evidence, PR to own fork, Loom recording |

## Order of delivery (PDF §3)

1. API counts from DB  
2. Page calls API  
3. Graph  
4. Empty + failed request UX  
5. Login + task access checks  
6. MO-1 latency objective  
7. `job_id` filter (skip plain count when set; document why)  
8–10. WebSocket + reconnect + decision record (if reached)

**Explicit skips if time runs out:** WebSocket (8–9) before MO-1 and filter are done; no item 10 decision record if WebSocket not attempted.

## Technical approach

- **Counts:** Aggregate `LabeledShape`, `LabeledImage`, and `LabeledTrack` for jobs under the task (`job.segment.task_id`), grouped by `label__name` (label on `Annotation.label` → `Label.name`).
- **API:** `GET /api/test/tasks/<task_id>/annotation-counts?job_id=` under new app `cvat.apps.test`.
- **Auth:** Reuse `TaskPermission` with `VIEW` scope for the task (same as viewing task metadata).
- **UI:** New route `/tasks/:tid/class-analytics`, `react-chartjs-2` bar chart.
- **Live updates (planned):** Django signals on annotation models → Redis pub/sub → ASGI WebSocket at `/api/test/ws/tasks/<task_id>/annotation-counts`.

## Rejected alternative (for item 10 if implemented)

**Rejected:** Client polling every N seconds.  
**Cost:** Simpler to ship but misses “live over WebSocket”, wastes server load, and hides disconnect/reconnect behaviour the brief asks for.

**Chosen:** Redis pub/sub + WebSocket (if completed).

## Plan changes

_(Update here if scope shifts; e.g. Docker RAM limits forcing smaller COCO subset.)_
