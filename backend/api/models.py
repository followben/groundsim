from datetime import datetime
from enum import Enum
from typing import Mapping, Optional

from pydantic import BaseModel


class GSPointType(str, Enum):
    """Groundstation telemetry types"""

    az = "az"
    el = "el"
    power = "power"


class GSPoint(BaseModel):
    """A groundstation telemetry point"""

    type: GSPointType
    timestamp: Optional[datetime]
    value: float


class GSPoints(BaseModel):
    """A list of groundstation telemetry points"""

    __root__: list[GSPoint]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]


class GSPointsIndexed(BaseModel):
    """Dict-like structure with lists of groundstation telemetry points keyed by the emit time in seconds"""

    __root__: Mapping[int, GSPoints]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]

    def keys(self):
        return self.__root__.keys()
