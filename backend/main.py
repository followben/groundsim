import json

import api.tasks as tasks
from api.models import GSPoints, GSPointsIndexed
from api.pubsub import broadcast
from api.routers import graphql_router
from fastapi import BackgroundTasks, FastAPI, Response, status
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(graphql_router, prefix="/graphql")

    @app.get("/latestpoints", response_model=GSPoints)
    async def get_latestpoints():
        return tasks.latestpoints

    @app.post("/simulation", status_code=status.HTTP_201_CREATED, response_class=Response)
    async def create_simulation(background_tasks: BackgroundTasks):
        if tasks.running:
            raise HTTPException(status.HTTP_409_CONFLICT, detail="Simulation already running")
        with open("tracking.json", "r") as f:
            data = GSPointsIndexed.parse_obj(json.load(f))
        background_tasks.add_task(tasks.new_simulation, data)

    @app.on_event("startup")
    async def startup():
        await broadcast.connect()

    @app.on_event("shutdown")
    async def shutdown():
        await broadcast.disconnect()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "https://gs.fly.dev",
            "http://localhost:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = create_app()
