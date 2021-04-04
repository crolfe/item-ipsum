import json
from http import HTTPStatus as status

from fastapi import HTTPException, FastAPI, Path, Response, Request

from src.db import InMemoryDB, NotFoundError
from src.templates import ItemTemplate, new_item

databases = {"templates": InMemoryDB()}

DEFAULT_NEW_ITEMS = 10

app = FastAPI()


def _generate_uri(path, pk):
    return f"/{path}/{pk}"


@app.get("/")
async def index():
    return {"status": "ok"}


@app.post("/_admin/templates/", status_code=status.CREATED)
async def create_template(resp: Response, template: ItemTemplate):
    pk = databases["templates"].insert(template)

    resp.headers["Location"] = _generate_uri("_admin/templates", pk)

    _create_items(template)


def _create_items(template: ItemTemplate, new_items: int = DEFAULT_NEW_ITEMS) -> None:
    global databases
    db = InMemoryDB()
    databases[template.name] = db

    for _ in range(DEFAULT_NEW_ITEMS + 1):
        item = new_item(template)
        db.insert(item)


@app.get("/_admin/templates/{template_id}")
async def get_template(resp: Response, template_id: str = Path(...)):
    try:
        template = databases["templates"].get(template_id)
    except NotFoundError:
        raise HTTPException(status_code=status.NOT_FOUND)

    return template


@app.get("/{item_type}/")
async def list_items(item_type: str = Path(...)):
    try:
        db = databases[item_type]
    except KeyError:
        err = f"A corresponding template was not found for a type of: {item_type}"
        raise HTTPException(status_code=status.NOT_FOUND, detail=err)

    data = db.list()[:DEFAULT_NEW_ITEMS]

    return {"data": data, "count": len(data)}


@app.post("/{item_type}/", status_code=status.CREATED)
async def create_item(req: Request, resp: Response, item_type: str = Path(...)):
    body = await req.body()

    try:
        db = databases[item_type]
    except KeyError:
        err = f"template not found for {item_type}. Did you create it?"
        raise HTTPException(status_code=status.NOT_FOUND, detail=err)

    pk = db.insert(json.loads(body))

    resp.headers["Location"] = _generate_uri(item_type, pk)


@app.get("/{item_type}/{pk}")
async def get_item(item_type: str, pk: str):
    try:
        db = databases[item_type]
        item = db.get(pk)
    except NotFoundError:
        err = f"{pk} not found"
        raise HTTPException(status_code=status.NOT_FOUND, detail=err)

    except KeyError:
        err = f"db not found for {item_type}. Did you create it?"
        raise HTTPException(status_code=status.NOT_FOUND, detail=err)

    return item


@app.put("/{item_type}/{pk}")
async def upsert_item(req: Request, item_type: str, pk: str):

    try:
        db = databases[item_type]
    except KeyError:
        err = f"db not found for {item_type}. Did you create it?"
        raise HTTPException(status_code=status.NOT_FOUND, detail=err)

    body = await req.body()
    item_data = json.loads(body)
    db.insert(item_data, pk=pk)
    return item_data


@app.delete("/{item_type}/{pk}", status_code=status.GONE)
async def delete_item(req: Request, item_type: str, pk: str):
    try:
        db = databases[item_type]
    except KeyError:
        err = f"db not found for {item_type}. Did you create it?"
        raise HTTPException(status_code=status.NOT_FOUND, detail=err)

    db.delete(pk)
