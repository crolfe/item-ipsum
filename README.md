_Item Ipsum_ makes it easy to stand up a REST API that can pre-generate data for you.
If you're building a web or mobile application, and you need to stand up a
simple CRUD backend, this is the tool for you.  Write a template that describes the
attsributes and types of your model, and let Item Ipsum do the rest!

### Requirements

* Docker and docker-compose are installed and working

### Setup and Usage

1. Bring up Item Ipsum: `docker-compose up --build`
2. Write a template per model(s) you want to work with.  Have a look at the `examples` directory for samples.
3. Make a POST to the `/_admin/templates/` endpoint to create your first template

  Example: Creating a `todos`
  ```
  > curl -X POST http://localhost:8000/_admin/templates/ -H 'Content-Type: application/json' -d @./examples/todos.json -i

  HTTP/1.1 201 Created
  date: Sat, 03 Apr 2021 22:56:14 GMT
  server: uvicorn
  content-length: 4
  content-type: application/json
  location: /_admin/templates/2b7cbfa50bd14bc7975b5aac3073ccbc
  ```
4. You can now access a list of `todos`:  `curl http://localhost:8000/todos`
5. GET/PUT/DELETE endpoints are also available to operate on a single `todo`
