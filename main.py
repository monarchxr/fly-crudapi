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