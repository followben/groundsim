import os

from broadcaster import Broadcast

BROADCAST_URL = os.environ.get("BROADCAST_URL", "memory://")

broadcast = Broadcast(BROADCAST_URL)

POINTS_CHANNEL = "points"
STATUS_CHANNEL = "status"
