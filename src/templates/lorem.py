from pydantic import BaseModel


class LoremArgs(BaseModel):
    nb: int = 3
