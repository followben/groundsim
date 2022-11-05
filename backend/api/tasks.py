import asyncio
from datetime import datetime

import api.pubsub as pubsub
from api.models import GSPoints, GSPointsIndexed
from broadcaster import Broadcast

latestpoints = GSPoints(__root__=[])
running: bool = False


async def _update_running(
    updated: bool,
    broadcast: Broadcast = pubsub.broadcast,
    status_channel: str = pubsub.STATUS_CHANNEL,
):
    global running
    if running == updated:
        return
    running = updated
    await broadcast.publish(channel=status_channel, message=running)


async def new_simulation(
    data: GSPointsIndexed,
    broadcast: Broadcast = pubsub.broadcast,
    points_channel: str = pubsub.POINTS_CHANNEL,
    status_channel: str = pubsub.STATUS_CHANNEL,
):
    """Publishes groundstation telemetry points to the specified broadcaster channel"""
    global running, latestpoints
    if running:
        return

    await _update_running(True, broadcast, status_channel)

    counter = 0
    emit_at = data.keys()

    while counter <= max(emit_at):
        if counter in emit_at:
            points = data[counter]
            for point in points:
                point.timestamp = datetime.utcnow()
                await broadcast.publish(channel=points_channel, message=point.json())
            latestpoints = points
        await asyncio.sleep(1)
        counter += 1

    await _update_running(False, broadcast, status_channel)
