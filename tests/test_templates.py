from datetime import datetime

import pytest
from dateutil.tz import tzutc

from src import templates


@pytest.fixture
def template_with_all_types():
    """
    A template that includes one of every possible type in ItemAttrType
    """
    data = {"name": "one-of-everything", "attrs": {}}
    for attr_type in templates.type_to_provider_method:
        data["attrs"][attr_type] = {"type": attr_type}

    return templates.ItemTemplate.parse_obj(data)


def test_all_types_are_registered_correctly(template_with_all_types):

    """
    This test is mostly just a sanity check to ensure everything is wired up correctly.
    """
    new_item = templates.new_item(template_with_all_types)
    assert new_item.keys() == template_with_all_types.dict()["attrs"].keys()


def test_datetime_no_args_returns_dt_in_past():
    now = datetime.now(tzutc()).isoformat()

    dt_in_past = templates.datetime()
    assert dt_in_past < now


def test_datetime_when_period_eq_past_returns_dt_in_past():
    now = datetime.now(tzutc()).isoformat()

    dt_in_past = templates.datetime(period="past")
    assert dt_in_past < now


def test_datetime_when_period_eq_future_returns_dt_in_future():
    now = datetime.now(tzutc()).isoformat()

    dt_in_future = templates.datetime(period="future")
    assert dt_in_future > now
