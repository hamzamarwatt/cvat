# Submission checklist (xis.ai assessment)

## Links to send in email

Replace `<YOUR_PR_NUMBER>` after opening the PR.

| Item | URL |
|------|-----|
| **Pull request** | https://github.com/hamzamarwatt/cvat/compare/main...dev-test01?expand=1 |
| **Branch** | https://github.com/hamzamarwatt/cvat/tree/dev-test01 |
| **Loom** | _(paste your recording link)_ |

## Email reply template

```
Subject: Re: Full Stack Assessment — submission

PR (fork dev-test01 → main): https://github.com/hamzamarwatt/cvat/pull/<YOUR_PR_NUMBER>
Loom (≤ 5 min): <LOOM_URL>

Setup and run: docs/SETUP.md (use docker-compose.podman.yml on Fedora/Podman).
Assessment docs: docs/Plan.md, docs/Objectives.md, docs/DefinitionOfDone.md

CVAT clone SHA (start): a81ed252dce15b805d5a544116cf98005e42f257
Branch tip (submission): see git log on dev-test01.

Acknowledged: 28 Oct 2026, 17:57 (UTC+5)
```

## Open the PR (GitHub UI)

1. https://github.com/hamzamarwatt/cvat/compare/main...dev-test01?expand=1  
2. Title: `Annotation analytics assessment (dev-test01)`  
3. Description: link to `docs/Plan.md`, list features (API, UI, auth, job filter, WebSocket).  
4. **Do not** open against `cvat-ai/cvat`.

## After CVAT is running — finish MO-1

```bash
./docs/benchmark_annotation_counts.sh <TASK_ID> '<sessionid>'
```

Paste output into `docs/Objectives.md`, commit, push, update PR.

## Run automated count tests (in container)

```bash
docker exec -it cvat_server bash -ic 'python3 ~/manage.py test cvat.apps.test.tests.test_services --keepdb'
```
