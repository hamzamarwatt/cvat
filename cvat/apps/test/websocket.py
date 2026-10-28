# Copyright (C) CVAT.ai Corporation
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import json

from asgiref.sync import sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.backends.db import SessionStore

from .realtime import (
    build_counts_payload,
    ensure_redis_listener,
    register_subscriber,
    unregister_subscriber,
    user_can_view_task,
)


def _user_from_scope(scope) -> AnonymousUser:
    headers = dict(scope.get("headers", ()))
    cookie_header = headers.get(b"cookie", b"").decode()
    session_key = None
    for part in cookie_header.split(";"):
        part = part.strip()
        if part.startswith("sessionid="):
            session_key = part.split("=", 1)[1]
            break

    if not session_key:
        return AnonymousUser()

    store = SessionStore(session_key=session_key)
    user_id = store.get("_auth_user_id")
    if not user_id:
        return AnonymousUser()

    from cvat.apps.iam.models import User

    try:
        return User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


async def annotation_counts_websocket(scope, receive, send) -> None:
    if scope["type"] != "websocket":
        return

    path = scope.get("path", "")
    parts = [p for p in path.split("/") if p]
    try:
        task_id = int(parts[parts.index("tasks") + 1])
    except (ValueError, IndexError):
        await send({"type": "websocket.close", "code": 4400})
        return

    await send({"type": "websocket.accept"})

    user = await sync_to_async(_user_from_scope)(scope)
    if not await user_can_view_task(user, task_id):
        await send({"type": "websocket.close", "code": 4403})
        return

    ensure_redis_listener()
    queue = await register_subscriber(task_id)

    initial = await build_counts_payload(task_id)
    await send({"type": "websocket.send", "text": json.dumps(initial)})

    async def forward_updates():
        while True:
            message = await queue.get()
            payload = json.loads(message)
            full = await build_counts_payload(int(payload["task_id"]))
            await send({"type": "websocket.send", "text": json.dumps(full)})

    forward_task = None
    try:
        import asyncio

        forward_task = asyncio.create_task(forward_updates())
        while True:
            event = await receive()
            if event["type"] == "websocket.disconnect":
                break
    finally:
        await unregister_subscriber(task_id, queue)
        if forward_task is not None:
            forward_task.cancel()
