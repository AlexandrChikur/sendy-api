import asyncio
from asyncio import Task
from typing import Any

from fastapi_websocket_pubsub.pub_sub_server import PubSubEndpoint


async def _task(*, endpoint: PubSubEndpoint, topic: str, data: Any) -> None:
    await endpoint.publish(topics=topic, data=data)


async def publish_content(*, endpoint: PubSubEndpoint, topic: str, data: Any) -> Task:
    return asyncio.create_task(_task(endpoint=endpoint, topic=topic, data=data))
