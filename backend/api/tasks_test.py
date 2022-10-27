import datetime
import json
from unittest.mock import patch

import pytest
from api.models import GSPointsIndexed
from api.tasks import run_simulation
from broadcaster import Broadcast


@pytest.fixture
def data():
    yield GSPointsIndexed.parse_obj({"0": [{"type": "el", "value": 5.0}]})


@pytest.fixture
def utcnow():
    utcnow = datetime.datetime(2022, 1, 1, 0, 0, 0)
    with patch("api.tasks.datetime") as mock:
        mock.utcnow.return_value = utcnow
        yield utcnow


async def test_broadcast_message(data: GSPointsIndexed, utcnow: datetime.datetime):
    async with Broadcast("memory://") as broadcast:
        channel = "test"
        async with broadcast.subscribe(channel) as subscriber:
            await run_simulation(data, broadcast, channel)
            event = await subscriber.get()  # type: ignore
            result = json.loads(event.message)
            assert result["type"] == "el"
            assert result["value"] == 5.0
            assert result["timestamp"] == utcnow.isoformat()
