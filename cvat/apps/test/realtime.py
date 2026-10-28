# Copyright (C) CVAT.ai Corporation
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import asyncio
import json
import logging
from collections import defaultdict
from typing import Any

from asgiref.sync import sync_to_async
from django.conf import settings

logger = logging.getLogger(__name__)

CHANNEL_PREFIX = "test:annotation_counts:task:"

_subscribers: dict[int, set[asyncio.Queue[str]]] = defaultdict(set)
_subscribers_lock = asyncio.Lock()


def _redis_client():
    import redis

    return redis.Redis.from_url(settings.REDIS_INMEM_URL, decode_responses=True)


def broadcast_task_counts(task_id: int) -> None:
    """Publish a change notification (sync, safe from Django signals)."""
    try:
        client = _redis_client()
        client.publish(f"{CHANNEL_PREFIX}{task_id}", json.dumps({"task_id": task_id}))
    except Exception:  # noqa: BLE001
        logger.exception("Failed to publish annotation count update for task %s", task_id)


async def register_subscriber(task_id: int) -> asyncio.Queue[str]:
    queue: asyncio.Queue[str] = asyncio.Queue()
    async with _subscribers_lock:
        _subscribers[task_id].add(queue)
    return queue


async def unregister_subscriber(task_id: int, queue: asyncio.Queue[str]) -> None:
    async with _subscribers_lock:
        _subscribers[task_id].discard(queue)
        if not _subscribers[task_id]:
            _subscribers.pop(task_id, None)


async def fanout_local(task_id: int, message: str) -> None:
    async with _subscribers_lock:
        targets = list(_subscribers.get(task_id, ()))
    for queue in targets:
        await queue.put(message)


async def redis_listener_loop() -> None:
    import redis.asyncio as aioredis

    client = aioredis.from_url(settings.REDIS_INMEM_URL, decode_responses=True)
    pubsub = client.pubsub()
    await pubsub.psubscribe(f"{CHANNEL_PREFIX}*")

    try:
        async for raw in pubsub.listen():
            if raw.get("type") != "pmessage":
                continue
            data = raw.get("data")
            if not isinstance(data, str):
                continue
            try:
                payload = json.loads(data)
                task_id = int(payload["task_id"])
            except (ValueError, KeyError, TypeError):
                continue
            await fanout_local(task_id, data)
    finally:
        await pubsub.close()
        await client.close()


_listener_started = False


def ensure_redis_listener() -> None:
    global _listener_started
    if _listener_started:
        return
    _listener_started = True

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    loop.create_task(redis_listener_loop())


async def user_can_view_task(user, task_id: int) -> bool:
    from django.http import HttpRequest
    from django.utils.functional import SimpleLazyObject

    from cvat.apps.iam.middleware import get_organization

    from .permissions import TaskAnnotationCountsPermission

    class _View:
        kwargs = {"task_id": task_id}

    @sync_to_async
    def check() -> bool:
        if not user or not getattr(user, "is_authenticated", False):
            return False

        request = HttpRequest()
        request.user = user
        request.method = "GET"
        request.iam_context = SimpleLazyObject(lambda: get_organization(request))

        permissions = TaskAnnotationCountsPermission.create(request, _View(), None, iam_context=None)
        return all(perm.check_access().allow for perm in permissions)

    return await check()


async def build_counts_payload(task_id: int) -> dict[str, Any]:
    from .services import compute_annotation_counts

    @sync_to_async
    def load():
        return {
            "task_id": task_id,
            "job_id": None,
            "counts": compute_annotation_counts(task_id=task_id),
        }

    return await load()
