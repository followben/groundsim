from typing import AsyncGenerator, AsyncIterable, cast

import api.pubsub as pubsub
import api.tasks as tasks
import strawberry
from api.graphql.types import GQLPoint
from api.models import GSPoint
from broadcaster import Event


def get_latest() -> list[GQLPoint]:
    return [GQLPoint.from_pydantic(p) for p in tasks.latestpoints]


@strawberry.type
class Query:
    latestpoints: list[GQLPoint] = strawberry.field(resolver=get_latest)


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def points(self) -> AsyncGenerator[GQLPoint, None]:
        async with pubsub.broadcast.subscribe(channel=pubsub.channel) as subscriber:
            async for event in cast(AsyncIterable[Event], subscriber):
                point = GSPoint.parse_raw(event.message)
                yield GQLPoint.from_pydantic(point)
