# Evidence — manual checks (run when CVAT is on :8080)

Set `TASK_ID` and `SESSION` (browser cookie `sessionid` after login).

## API success

```bash
curl -s -H "Cookie: sessionid=${SESSION}" \
  "http://localhost:8080/api/test/tasks/${TASK_ID}/annotation-counts" | jq .
```

Expected shape:

```json
{"task_id": 1, "job_id": null, "counts": [{"label": "person", "count": 42}, ...]}
```

## Item 5 — unauthenticated (401)

```bash
curl -s -o /dev/null -w "%{http_code}\n" \
  "http://localhost:8080/api/test/tasks/${TASK_ID}/annotation-counts"
```

Expected: `401`

## Item 6 — no access (403)

Log in as a user **without** access to the task, copy their `sessionid`, then:

```bash
curl -s -o /dev/null -w "%{http_code}\n" \
  -H "Cookie: sessionid=${OTHER_SESSION}" \
  "http://localhost:8080/api/test/tasks/${TASK_ID}/annotation-counts"
```

Expected: `403`

## Item 8 — job filter

```bash
curl -s -H "Cookie: sessionid=${SESSION}" \
  "http://localhost:8080/api/test/tasks/${TASK_ID}/annotation-counts?job_id=${JOB_ID}" | jq .
```

## Unit tests (no UI)

Inside `cvat_server` container after deploy:

```bash
python3 ~/manage.py test cvat.apps.test.tests.test_services -v2
```
