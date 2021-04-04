from pprint import pprint

import requests

from invoke import task  # type: ignore


@task
def compile(c):
    # run this if bumping an app and/or dev dependency
    # produces requirements.txt and requirements-dev.txt
    c.run("pip-compile requirements.in")
    c.run("pip-compile requirements-dev.in")


@task
def test(c):
    c.run("pytest", env={"PYTHONPATH": "."})


@task
def run(c):
    c.run("docker-compose up --build")


@task
def create_template(c):
    data = {
        "name": "todos",
        "description": "A collection of tasks on a todo list",
        "attrs": {
            "title": {"type": "string"},
            "is_complete": {"type": "bool"},
            "description": {"type": "sentence"},
            "priority": {"type": "int", "args": {"min_value": 1, "max_value": 5}},
            "due_date": {"type": "datetime", "args": {"period": "future"}},
            "created": {"type": "datetime", "args": {"period": "past"}}
        },
    }

    resp = requests.post("http://localhost:8000/_admin/templates/", json=data)
    resp.raise_for_status()  # show an error if non-200 response

    print("Successfully created a todos template")


@task
def get_items(c):
    resp = requests.get("http://localhost:8000/todos/")
    resp.raise_for_status()

    pprint(resp.json())
