# Objectives

**Environment:**

| Field | Value |
|-------|--------|
| OS | Linux 6.19.10-300.fc44.x86_64 (Fedora 44) |
| CPU | Intel Core i5-7300U @ 2.60GHz (4 threads) |
| RAM | 7.6 GiB |
| CVAT clone SHA (assessment start) | `a81ed252dce15b805d5a544116cf98005e42f257` |
| Submission branch tip | `dev-test01` (see latest commit on fork) |
| Sample data | COCO val2017 subset — count in `DefinitionOfDone.md` after upload |

## MO-1 — Annotation counts API latency

| ID | Field | Entry |
|----|-------|--------|
| MO-1 | What is measured | Wall time for `GET /api/test/tasks/<task_id>/annotation-counts` to return HTTP 200 with JSON body |
| MO-1 | How | `docs/benchmark_annotation_counts.sh` — curl with session cookie, 5 runs, median reported |
| MO-1 | Target | Median ≤ **250 ms** on local Docker/Podman stack with assessment dataset |
| MO-1 | Conditions | Same task ID, no `job_id` filter, logged-in user with task access, stack fully up, no cold migration |
| MO-1 | Not included | WebSocket traffic, first request after container start, image build time |

### Raw results

Run when CVAT responds on port 8080:

```bash
cd cvat
./docs/benchmark_annotation_counts.sh <TASK_ID> '<sessionid>'
```

Paste **full terminal output** below (required for a complete MO-1; do not estimate numbers):

```
(pending — CVAT stack was still building on Podman at documentation time; re-run script, paste output, commit, push)
```

**Median / spread:** _(pending raw runs)_

**Target met?** _(pending — yes/no + one sentence after measurement)_

### If deadline passes before measurement

State in submission email: MO-1 script and endpoint are in repo; raw runs were blocked by local Podman/registry build time; candidate will append results to `Objectives.md` in the PR if the stack completes within minutes of submit.
