from typing import Optional, Union

from pydantic import BaseModel

Number = Union[int, float]


class StringArgs(BaseModel):
    min_chars: Optional[int] = None
    max_chars: Optional[int] = 20


class IntArgs(BaseModel):
    min_value: int = 0
    max_value: int = 9999
    step: int = 1


class FloatArgs(BaseModel):
    positive: bool = False  # only allow positive numbers if set True
    min_value: Optional[Number] = None
    max_value: Optional[Number] = None
