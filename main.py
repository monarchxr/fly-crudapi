from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

tasklist = [
    {
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
    }
]

@app.get("/")
async def root():
    return{
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks", "/tasks/{task_id}", "/health"]
        }

@app.get("/health")
async def health():
    return{
        "status": "ok"
    }

@app.get("/tasks")
async def tasks():
    return tasklist

@app.get("/tasks/{task_id}")
async def get_task(task_id: int):

    task_with_id = None

    for task in tasklist:
        if task["id"]==task_id:
            task_with_id = task
            break

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

    task_title = body.get("title") or None
    task_status = body.get("done") or None

    if not task_title and not task_status:
        return JSONResponse(status_code=400, content={"Bad Request": "Empty/invalid body"})

    tid = task_id
    task_with_id = None

    for task in tasklist:
        if task["id"]==tid:
            task_with_id = task
            break

    if not task_with_id:
        return JSONResponse(status_code=404, content={"Bad Request": "Unknown id"})

    if task_title:
        task_with_id["title"] = task_title
    if task_status:
        task_with_id["done"] = task_status

    return JSONResponse(status_code=200, content={"Updated": task_with_id})

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):

    for task in tasklist:
        if task["id"] == task_id:
            tasklist.remove(task)
            return JSONResponse(status_code=201, content={"Deleted": task})

    return JSONResponse(status_code=404, content={"Bad Request": "Unknown id"})