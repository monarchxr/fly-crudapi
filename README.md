# fly-crudapi

## What this is
Simple CRUD API that manages a task list

You can create, read, update, and delete tasks

Data now lives inside a SQLite database and persists even after server restarted

## How to install and run it
To install just

```git clone https://github.com/monarchxr/fly-crudapi.git```

To run it

```uv run fastapi dev```

## Endpoints

| Endpoint 1 | Endpoint 2 | Endpoint 3| Endpoint 4 | Endpoint 5 | Endpoint 6 |
| ---------- | ---------- | --------- | ---------- | ---------- | ---------- |
| /health | /tasks | /tasks/{id} | /tasks/ | /stats | /reset |

## Why SQLite was chosen
We chose SQLite because it is lightweight and serverless

## Where the database file is stored
Currently it is stored in the main repo folder, named as "tasks.db"

## Database Viewer (DB Browser)
![dbview](assets/dbview.png)

## Sample curl output
![curl](assets/curl_output.png)


## Swagger UI screenshot
![swagger](assets/SwaggerUI.png)