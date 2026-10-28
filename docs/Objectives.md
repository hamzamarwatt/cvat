# Objectives

**Environment (fill when measured):**

| Field | Value |
|-------|--------|
| OS | Linux 6.19.10-300.fc44.x86_64 |
| CPU | Intel Core i5-7300U @ 2.60GHz (4 threads) |
| RAM | 7.6 GiB |
| CVAT SHA | `a81ed252dce15b805d5a544116cf98005e42f257` |
| Sample data | COCO val2017 subset — _image count recorded in Definition of Done_ |

## MO-1 — Annotation counts API latency

| ID | Field | Entry |
|----|-------|--------|
| MO-1 | What is measured | Wall time for `GET /api/test/tasks/<task_id>/annotation-counts` to return HTTP 200 with JSON body |
| MO-1 | How | `docs/benchmark_annotation_counts.sh` — curl with session cookie, 5 runs |
| MO-1 | Target | Median ≤ **250 ms** on local Docker stack with assessment dataset |
| MO-1 | Conditions | Same task ID, no `job_id` filter, Chrome/curl, CVAT logged in as admin/superuser, no other heavy jobs |
| MO-1 | Not included | WebSocket traffic, cold Docker first start, first request after DB migration |

**Raw results:** pasted below after measurement on the submission machine.

```
(pending — run docs/benchmark_annotation_counts.sh after stack is up)
```

**Median / spread:** _(pending)_

**Target met?** _(pending — yes/no + reason)_
