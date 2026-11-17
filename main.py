import sqlite3
from contextlib import asynccontextmanager
from fastapi import FastAPI, Response, Depends
from fastapi.responses import JSONResponse

@asynccontextmanager                                # turns the function below into a startup/shutdown manager
async def lifespan(app: FastAPI):
    conn = sqlite3.connect("tasks.db")              # opens or creates database file
    cursor = conn.cursor()                          # creates a cursor object to execute SQL commands

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                title TEXT,
                done BOOLEAN
            )
    """)

    cursor.execute("SELECT 1 FROM tasks LIMIT 1")
    is_empty = cursor.fetchone() is None

    if is_empty:
        seed_tasks = [("Set up database", 1), ("Build API endpoints", 1), ("Test endpoints", 0),]

        cursor.executemany("INSERT INTO tasks (title, done) VALUES (?, ?)",seed_tasks)

    conn.commit()                                   # save table creation permanently to db file
    conn.close()                                    # close db conn so file is not locked

    yield                                           # pause while server runs and handles requests
    print("Server shutting down")

app = FastAPI(lifespan=lifespan)

def get_db():
    conn = sqlite3.connect("tasks.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row

    try:
        yield conn
    finally:
        conn.close()


@app.get("/")
async def root():
    return{
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks", "/tasks/{task_id}", "/health", "/tasks/", "/stats", "/reset"]
        }

@app.get("/health")
async def health():
    return{
        "status": "ok"
    }

@app.get("/tasks")
async def tasks(db: sqlite3.Connection = Depends(get_db)):
    tasks = db.execute("SELECT * FROM tasks").fetchall()
    return tasks

@app.get("/tasks/{task_id}")
async def get_task(task_id: int, db: sqlite3.Connection = Depends(get_db)):

    task_with_id = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()

    if task_with_id is None:
        return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
    
    return task_with_id

@app.post("/tasks")
async def add_task(body: dict):
    task_title = body.get("title") or None

    if not task_title:
        return JSONResponse(status_code=400, content={"Bad Request": "task title cannot be empty"})

    new_id = tasklist[-1]["id"]+1 if tasklist else 1

    new_task = {"id": new_id, "title": task_title, "done": False}

    tasklist.append(new_task)

    return JSONResponse(status_code=201, content={"Created": new_task})

@app.put("/tasks/{task_id}")
async def replace_task(body: dict, task_id: int):

    task_title = body.get("title")
    task_status = body.get("done")

    if not task_title and task_status is None:
        return JSONResponse(status_code=400, content={"Bad Request": "Empty/invalid body"})

    if task_status is not None and not isinstance(task_status, bool):
        return JSONResponse(status_code=400, content={"Bad Request": "'done' must be a boolean"})

    task_with_id = None

    for task in tasklist:
        if task["id"]==task_id:
            task_with_id = task
            break

    if not task_with_id:
        return JSONResponse(status_code=404, content={"Bad Request": "Unknown id"})

    if task_title:
        task_with_id["title"] = task_title
    if task_status is not None:
        task_with_id["done"] = task_status

    return JSONResponse(status_code=200, content={"Updated": task_with_id})

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):

    for task in tasklist:
        if task["id"] == task_id:
            tasklist.remove(task)
            return Response(status_code=204)

    return JSONResponse(status_code=404, content={"Bad Request": "Unknown id"})

@app.get("/tasks/")
def group_tasks_by_status(done: bool=False):
    task_required = []

    for task in tasklist:
        if task["done"]==done:
            task_required.append(task)

    if task_required:
        return JSONResponse(status_code=200, content={"Tasks are as follows": task_required})

@app.get("/stats")
def calculate_stats():
    total = len(tasklist)
    done = 0
    open = 0

    for task in tasklist:
        if task["done"] is True:
            done+=1
    
    open = total - done

    return JSONResponse(status_code=200, content={"total": total, "done": done, "open": open})

@app.post("/reset")
def reset_tasks():

    sample_tasks = [{
            "id": 1,
            "title": "Create setup",
            "done": True
        },
    
        {
            "id": 2,
            "title": "Create task list",
            "done": True
        },
    
        {
            "id": 3,
            "title": "Complete API work",
            "done": False
        }]

    tasklist.clear()
    tasklist.extend(sample_tasks)

    return JSONResponse(status_code=201, content={"message": "Tasks reset to  default 3 tasks successfully", "tasks": tasklist})