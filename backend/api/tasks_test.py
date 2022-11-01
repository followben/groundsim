import datetime
import json
from unittest.mock import patch

import pytest
from api.models import GSPointsIndexed
from api.tasks import new_simulation
from broadcaster import Broadcast


@pytest.fixture
def channel(request: pytest.FixtureRequest):
    yield request.node.name


@pytest.fixture
def data():
    yield GSPointsIndexed.parse_obj({"0": [{"type": "el", "value": 5.0}]})


@pytest.fixture
def utcnow():
    utcnow = datetime.datetime(2022, 1, 1, 0, 0, 0)
    with patch("api.tasks.datetime") as mock:
        mock.utcnow.return_value = utcnow
        yield utcnow


async def test_run_simultation_broadcasts_data(data: GSPointsIndexed, channel: str, utcnow: datetime.datetime):
    async with Broadcast("memory://") as broadcast:
        async with broadcast.subscribe(channel) as subscriber:
            await new_simulation(data, broadcast, channel)
            event = await subscriber.get()  # type: ignore
            result = json.loads(event.message)
            assert result["type"] == "el"
            assert result["value"] == 5.0
            assert result["timestamp"] == utcnow.isoformat()
