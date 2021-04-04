from enum import Enum
from typing import Dict, Optional

from pydantic import BaseModel, Field


class ItemAttrType(Enum):
    string = "string"
    bool = "bool"
    float = "float"
    int = "int"
    datetime = "datetime"
    sentence = "sentence"
    sentences = "sentences"
    paragraph = "paragraph"
    paragraphs = "paragraphs"


class ItemAttr(BaseModel):
    type: ItemAttrType = Field(...)
    args: Optional[dict]

    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        data["type"] = self.type.value

        return data


class ItemTemplate(BaseModel):
    name: str
    description: Optional[str] = ""
    attrs: Dict[str, ItemAttr]
