import pytest

from src.db import InMemoryDB
from src.templates import ItemAttrType, ItemTemplate


@pytest.fixture
def db():
    _db = InMemoryDB()

    yield _db

    # clear DB at the end of a test run
    _db._items = {}


@pytest.fixture
def item_data():
    return {"foo": "bar"}


@pytest.fixture
def item_pk(db, item_data):
    return db.insert(item_data)


@pytest.fixture
def valid_template():
    return ItemTemplate.parse_obj(
        {
            "name": "todos",
            "description": "An item on a TODO list",
            "attrs": {
                "title": {"type": ItemAttrType.string.value},
                "priority": {"type": "int", "args": {"min_value": 1, "max_value": 5}},
                "is_complete": {"type": "bool"},
            },
        }
    )


@pytest.fixture
def valid_template_with_args():
    return ItemTemplate.parse_obj(
        {
            "name": "todos",
            "description": "An item on a TODO list",
            "attrs": {
                "title": {
                    "type": ItemAttrType.string.value,
                    "args": {"min_chars": 5, "max_chars": 10},
                }
            },
        }
    )
