import uuid

import pytest

from src.db import NotFoundError


def test_insert(db):
    item_data = {"foo": "bar"}
    pk = uuid.uuid4().hex

    db.insert(item_data, pk=pk)

    assert db.count() == 1


def test_get(db, item_data, item_pk):
    assert db.get(item_pk) == item_data


def test_get_not_found(db):
    with pytest.raises(NotFoundError):
        return db.get("does-not-exist")


def test_list(db, item_data, item_pk):
    resp = db.list()
    assert resp == [dict(pk=item_pk, **item_data)]
