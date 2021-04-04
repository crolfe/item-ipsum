from http import HTTPStatus as status

import pytest

from fastapi.testclient import TestClient
from src.api import app
from src.templates import new_item

templates_uri = "/_admin/templates/"


@pytest.fixture
def client():
    yield TestClient(app)


def test_index_get(client):
    resp = client.get("/")

    assert resp.status_code == status.OK
    assert resp.json() == {"status": "ok"}


def test_create_item_template(client):
    data = {
        "name": "todos",
        "description": "An item on a TODO list",
        "attrs": {"title": {"type": "string", "args": None}},
    }
    resp = client.post(templates_uri, json=data)

    assert resp.status_code == status.CREATED
    resp = client.get(resp.headers["Location"])
    assert resp.status_code == status.OK
    assert resp.json() == data, resp.json()

    resp = client.get("/todos/")
    assert resp.status_code == status.OK
    contents = resp.json()
    assert len(contents["data"]) == 10 == contents["count"]


def test_get_item_template_doesnt_exist(client):
    resp = client.get(f"{templates_uri}/does-not-exist")
    assert resp.status_code == status.NOT_FOUND


def test_create_update_delete_item(client, valid_template):
    # Create the template
    resp = client.post(templates_uri, json=valid_template.dict())

    # Create an item
    new_item_data = new_item(valid_template)
    item_resp = client.post(f"/{valid_template.name}/", json=new_item_data)
    assert item_resp.status_code == status.CREATED

    item_url = item_resp.headers["Location"]
    resp = client.get(item_url)
    assert resp.status_code == status.OK
    assert resp.json() == new_item_data

    # Update it
    updated_item_data = resp.json()
    updated_item_data["title"] = "new-title"
    resp = client.put(item_url, json=updated_item_data)
    assert resp.status_code == status.OK
    assert resp.json() == updated_item_data

    # Delete it
    resp = client.delete(item_url)
    assert resp.status_code == status.GONE

    resp = client.get(item_url)
    assert resp.status_code == status.NOT_FOUND
