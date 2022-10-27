import asyncio
from datetime import datetime

import api.pubsub as pubsub
from api.models import GSPoints, GSPointsIndexed

latestpoints = GSPoints(__root__=[])
_running: bool = False


async def run_simulation(data: GSPointsIndexed, channel: str = pubsub.channel):
    """Publishes groundstation telemetry points to the specified channel"""
    global _running, latestpoints
    if _running:
        return
    _running = True

    counter = 0
    emit_at = data.keys()

    while counter <= max(emit_at):
        if counter in emit_at:
            points = data[counter]
            for point in points:
                point.timestamp = datetime.utcnow()
                await pubsub.broadcast.publish(channel=channel, message=point.json())
            latestpoints = points
        await asyncio.sleep(1)
        counter += 1

    _running = False