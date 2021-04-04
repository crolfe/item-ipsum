from typing import Any, Dict, Optional

import faker  # type: ignore
import faker.providers  # type: ignore

from dateutil.tz import tzutc
from faker.providers.lorem.la import Provider as LoremProvider  # type: ignore
from pydantic import ValidationError

from src.exceptions import InvalidTemplateError
from src.templates.base import ItemAttrType, ItemTemplate
from src.templates.datetime import DatetimeArgs, Period
from src.templates.lorem import LoremArgs
from src.templates.python import FloatArgs, IntArgs, StringArgs


_faker = faker.Faker()

providers = {
    "python": faker.providers.python.Provider(_faker),
    "datetime": faker.providers.date_time.Provider(_faker),
    "lorem": LoremProvider(_faker),
}


def datetime(period: Optional[str] = None) -> str:
    if period == Period.future.value:
        dt = providers["datetime"].future_datetime(tzinfo=tzutc())
    else:
        # `period` is None or Period.past
        dt = providers["datetime"].past_datetime(tzinfo=tzutc())

    return dt.isoformat()


type_to_provider_method = {
    ItemAttrType.string.value: providers["python"].pystr,
    ItemAttrType.bool.value: providers["python"].pybool,
    ItemAttrType.int.value: providers["python"].pyint,
    ItemAttrType.float.value: providers["python"].pyfloat,
    ItemAttrType.datetime.value: datetime,
    ItemAttrType.sentence.value: providers["lorem"].sentence,
    ItemAttrType.sentences.value: providers["lorem"].sentences,
    ItemAttrType.paragraph.value: providers["lorem"].paragraph,
    ItemAttrType.paragraphs.value: providers["lorem"].paragraphs,
}

args_models = {
    ItemAttrType.string.value: StringArgs,
    ItemAttrType.float.value: FloatArgs,
    ItemAttrType.int.value: IntArgs,
    ItemAttrType.datetime.value: DatetimeArgs,
    ItemAttrType.sentences.value: LoremArgs,
    ItemAttrType.paragraphs.value: LoremArgs,
}


def valid_template(template: ItemTemplate) -> bool:
    for attr in template.attrs.values():
        # will raise an exception if invalid

        try:
            if attr.type in args_models and attr.args is not None:
                # not all types take arguments, but most do
                _class = args_models[str(attr.type)]
                _class.parse_obj(attr.args)
        except ValidationError:
            return False

    return True


def new_item(template: ItemTemplate) -> Dict[str, Any]:
    if not valid_template(template):
        raise InvalidTemplateError

    item = {}

    for attr, attr_meta in template.attrs.items():
        _type = attr_meta.type.value
        kwargs = attr_meta.args if attr_meta.args is not None else {}
        attr_value = type_to_provider_method[_type](**kwargs)
        item[attr] = attr_value

    return item
