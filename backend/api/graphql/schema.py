import json
from typing import AsyncGenerator, AsyncIterable, cast

import api.pubsub as pubsub
import api.tasks as tasks
import strawberry
from api.graphql.types import GQLPoint
from api.models import GSPoint, GSPointsIndexed
from broadcaster import Event
from strawberry.types import Info


def get_latest() -> list[GQLPoint]:
    return [GQLPoint.from_pydantic(p) for p in tasks.latestpoints]


@strawberry.type
class Query:
    latestpoints: list[GQLPoint] = strawberry.field(resolver=get_latest)


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def points(self) -> AsyncGenerator[GQLPoint, None]:
        async with pubsub.broadcast.subscribe(channel=pubsub.POINTS_CHANNEL) as subscriber:
            async for event in cast(AsyncIterable[Event], subscriber):
                point = GSPoint.parse_raw(event.message)
                yield GQLPoint.from_pydantic(point)

    @strawberry.subscription
    async def running(self) -> AsyncGenerator[bool, None]:
        async with pubsub.broadcast.subscribe(channel=pubsub.STATUS_CHANNEL) as subscriber:
            async for event in cast(AsyncIterable[Event], subscriber):
                yield event.message


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_simulation(self, info: Info) -> bool:
        if tasks.running:
            return False
        with open("tracking.json", "r") as f:
            data = GSPointsIndexed.parse_obj(json.load(f))
        info.context["background_tasks"].add_task(tasks.new_simulation, data)
        return True


schema = strawberry.Schema(query=Query, subscription=Subscription, mutation=Mutation)
