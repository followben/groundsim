import asyncio

from fastapi import FastAPI

app = FastAPI()


class BackgroundRunner:
    def __init__(self):
        self.value = 0

    async def run_main(self):
        while True:
            await asyncio.sleep(0.1)
            self.value += 1


runner = BackgroundRunner()


@app.on_event("startup")
async def app_startup():
    asyncio.create_task(runner.run_main())


@app.get("/")
def root():
    return runner.value
