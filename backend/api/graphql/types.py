from enum import Enum

import strawberry
from api.models import GSPoint, GSPoints


@strawberry.enum
class GQLPointType(str, Enum):
    az = "az"
    el = "el"
    power = "power"


@strawberry.experimental.pydantic.type(model=GSPoint)
class GQLPoint:
    type: GQLPointType
    timestamp: strawberry.auto
    value: strawberry.auto


@strawberry.experimental.pydantic.type(model=GSPoints, all_fields=True)
class GQLTelemetry:
    ...
