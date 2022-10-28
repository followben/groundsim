import json

import pytest
from api.models import GSPoints
from pydantic import ValidationError


def test_list_parses_array_of_points():
    data = json.dumps([{"type": "el", "value": 5.0}, {"type": "az", "value": 90.0}])
    points = GSPoints.parse_raw(data)
    assert len(points) == 2


def test_list_validates_malformed_points():
    data = json.dumps([{"type": "bob", "value": 5.0}, {"type": "az", "value": 90.0}])
    with pytest.raises(ValidationError):
        GSPoints.parse_raw(data)
