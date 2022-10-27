import asyncio
import json
from datetime import datetime

from api.models import GSPoints, Simulation
from api.pubsub import broadcast

latestpoints = GSPoints(__root__=[])
running: bool = False


async def simulation():
    global running, latestpoints
    if running:
        return
    running = True

    with open("tracking.json", "r") as f:
        data = Simulation.parse_obj(json.load(f))

    counter = 0
    emit_at = data.keys()

    while counter <= max(emit_at):
        if counter in emit_at:
            points = data[counter]
            for point in points:
                point.timestamp = datetime.utcnow()
                await broadcast.publish(channel="points", message=point.json())
            latestpoints = points
        await asyncio.sleep(1)
        counter += 1
