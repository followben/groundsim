import asyncio
import json
import os
from enum import Enum
from typing import AsyncGenerator, Mapping, Optional

import strawberry
from broadcaster import Broadcast
from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel
from strawberry.fastapi import GraphQLRouter

BROADCAST_URL = os.environ.get("BROADCAST_URL", "memory://")

broadcast = Broadcast(BROADCAST_URL)


@strawberry.enum
class GSPointType(str, Enum):
    az = "az"
    el = "el"
    power = "power"


class GSPoint(BaseModel):
    type: GSPointType
    value: float


class GSTelemetry(BaseModel):
    __root__: list[GSPoint]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]


class SimulationDict(BaseModel):
    __root__: Mapping[int, GSTelemetry]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]

    def keys(self):
        return self.__root__.keys()


running: bool = False
current: Optional[GSTelemetry] = None


@strawberry.experimental.pydantic.type(model=GSPoint, all_fields=True)
class GQLPoint:
    ...


@strawberry.experimental.pydantic.type(model=GSTelemetry, all_fields=True)
class GQLTelemetry:
    ...


def get_latest() -> list[GQLPoint]:
    return [GQLPoint.from_pydantic(p) for p in current] if current else []


@strawberry.type
class Query:
    latestpoints: list[GQLPoint] = strawberry.field(resolver=get_latest)


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def points(self) -> AsyncGenerator[GQLPoint, None]:
        async with broadcast.subscribe(channel="telemetry") as subscriber:
            async for event in subscriber:
                point = GSPoint.parse_raw(event.message)
                yield GQLPoint.from_pydantic(point)


schema = strawberry.Schema(query=Query, subscription=Subscription)

graphql_app = GraphQLRouter(schema)


async def simulate_overpass():
    global running, current
    if running:
        return
    running = True

    with open("tracking.json", "r") as f:
        data = SimulationDict.parse_obj(json.load(f))

    counter = 0
    emit_at = data.keys()

    while counter <= max(emit_at):
        if counter in emit_at:
            current = data[counter]
            for point in current:
                await broadcast.publish(channel="telemetry", message=point.json())
        await asyncio.sleep(1)
        counter += 1

    current = None


app = FastAPI()

app.include_router(graphql_app, prefix="/graphql")


@app.on_event("startup")
async def app_startup():
    await broadcast.connect()


@app.on_event("shutdown")
async def shutdown_event():
    await broadcast.disconnect()


@app.get("/")
async def get_current():
    return current


@app.post("/simulation")
async def create_simulation(background_tasks: BackgroundTasks):
    background_tasks.add_task(simulate_overpass)
