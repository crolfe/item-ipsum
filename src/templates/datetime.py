from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Period(Enum):
    past = "past"
    future = "future"


class DatetimeArgs(BaseModel):
    when: Optional[Period] = Field(...)
