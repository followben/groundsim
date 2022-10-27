from datetime import datetime
from enum import Enum
from typing import Mapping, Optional

from pydantic import BaseModel


class GSPointType(str, Enum):
    az = "az"
    el = "el"
    power = "power"


class GSPoint(BaseModel):
    type: GSPointType
    timestamp: Optional[datetime]
    value: float


class GSPoints(BaseModel):
    __root__: list[GSPoint]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]


class Simulation(BaseModel):
    __root__: Mapping[int, GSPoints]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]

    def keys(self):
        return self.__root__.keys()
