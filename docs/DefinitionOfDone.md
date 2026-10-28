# Definition of Done

Checklist written before implementation; evidence added at submission.

| # | Criterion | Done | Evidence |
|---|-----------|------|----------|
| 1 | Endpoint returns correct per-class counts for a known task | ☐ | Manual: compare total to CVAT job summary / spot-check labels — _link or task id_ |
| 2 | UI page renders bar chart for counts | ☐ | Screenshot or Loom timestamp |
| 3 | UI shows empty state when task has no annotations | ☐ | Screenshot / Loom |
| 4 | UI shows error state when API fails | ☐ | Screenshot (e.g. wrong task / network) / Loom |
| 5 | Unauthenticated request rejected | ☐ | `curl` without cookie → 401 — paste in PR or here |
| 6 | User without task access rejected | ☐ | Second user curl → 403 — paste |
| 7 | MO-1 measured (5 runs, raw output) | ☐ | See `docs/Objectives.md` |
| 8 | `job_id` query filter documented and working | ☐ | Example URL + sample JSON |
| 9 | WebSocket live update (if attempted) | ☐ | Loom demo |
| 10 | WebSocket reconnect (if attempted) | ☐ | Loom demo |
| 11 | Incremental git history (no single dump commit) | ☐ | `git log --oneline` on `dev-test01` |
| 12 | PR to **own fork** `main`, not upstream CVAT | ☐ | PR URL |
| 13 | Loom ≤ 5 min, K1–K4 answered | ☐ | Loom URL |
| 14 | Work not finished listed with reasons | ☐ | Section below |

## Not finished / deferred

_(Fill at end of 8 h window.)_

## Sample dataset

- COCO 2017 val images uploaded: _count TBD_
- Annotations: `instances_val2017.json` via Upload annotations → COCO 1.0
