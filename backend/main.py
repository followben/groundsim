import json

import api.tasks as tasks
from api.models import GSPoints, GSPointsIndexed
from api.pubsub import broadcast
from api.routers import graphql_router
from fastapi import BackgroundTasks, FastAPI, Response, status


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(graphql_router, prefix="/graphql")

    @app.get("/latestpoints", response_model=GSPoints)
    async def get_latestpoints():
        return tasks.latestpoints

    @app.post("/simulation", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
    async def create_simulation(background_tasks: BackgroundTasks):
        with open("tracking.json", "r") as f:
            data = GSPointsIndexed.parse_obj(json.load(f))
        background_tasks.add_task(tasks.run_simulation, data)

    @app.on_event("startup")
    async def startup():
        await broadcast.connect()

    @app.on_event("shutdown")
    async def shutdown():
        await broadcast.disconnect()

    return app


app = create_app()
