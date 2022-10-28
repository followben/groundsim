import datetime
import json
from unittest.mock import patch

import pytest
from api.graphql.schema import schema
from api.models import GSPoints


@pytest.fixture
def latestpoints():
    utcnow = datetime.datetime(2022, 1, 1, 0, 0, 0)
    data = GSPoints.parse_obj([{"type": "el", "timestamp": utcnow, "value": 5.0}])
    with patch("api.graphql.schema.tasks") as mock:
        mock.latestpoints = data
        yield data


def test_query(latestpoints: GSPoints):
    query = """
        query {
            latestpoints {
                type
                timestamp
                value
            }
        }
    """
    result = schema.execute_sync(query)
    assert result.errors is None
    assert result.data is not None
    assert result.data["latestpoints"] == json.loads(latestpoints.json())
