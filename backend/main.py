import asyncio
import json
from typing import Literal, Mapping, Optional

import strawberry
from fastapi import FastAPI
from pydantic import BaseModel
from strawberry.fastapi import GraphQLRouter


class TrackingPoint(BaseModel):
    type: Literal["az", "el", "power"]
    value: float


class TrackingPoints(BaseModel):
    __root__: Mapping[int, list[TrackingPoint]]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]

    def keys(self):
        return self.__root__.keys()


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"


schema = strawberry.Schema(Query)

graphql_app = GraphQLRouter(schema)


class AntennaSim(object):

    value: Optional[TrackingPoint] = None
    _points: Optional[TrackingPoints] = None
    _offset = 0

    @property
    def points(self) -> TrackingPoints:
        if not self._points:
            with open("tracking.json", "r") as f:
                self._points = TrackingPoints.parse_obj(json.load(f))
        return self._points

    async def run_main(self):
        while True:
            if self.points:
                if self._offset in self.points.keys():
                    new_points = self.points[self._offset]
                    self.value = new_points[0]
            await asyncio.sleep(1)
            self._offset += 1


sim = AntennaSim()

app = FastAPI()

app.include_router(graphql_app, prefix="/graphql")


@app.on_event("startup")
async def app_startup():
    asyncio.create_task(sim.run_main())


@app.get("/")
def root():
    result = sim.value.dict()
    return result
