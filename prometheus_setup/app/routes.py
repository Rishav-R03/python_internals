from fastapi import APIRouter,HTTPException
from pydantic import BaseModel 
from typing import Dict 

from .metrics import(
    TASKS_IN_PROGRESS,
    TASKS_CREATED_TOTAL,
    ERROR_COUNT
)

routes = APIRouter(prefix="/tasks",tags=["tasks"])

_tasks:Dict[int,dict] = {}
_next_id = 1 

class TaskCreate(BaseModel):
    title:str 
    priority: str = "medium"

class Task(BaseModel):
    id:int 
    title:str 
    priority:str 
    done: bool = False 

@routes.post("",response_model=Task,status_code=201)
def create_task(payload:TaskCreate):
    global _next_id
    if not payload.title.strip():
        ERROR_COUNT.labels(error_type="empty_title").inc()
        raise HTTPException(status_code=400,detail="Title cannot be empty")
    task ={
        "id": _next_id,
        "title":payload.title,
        "priority":payload.priority,
        "done":False,
    }
    _tasks[_next_id] = task 
    _next_id += 1

    TASKS_CREATED_TOTAL.inc()
    TASKS_IN_PROGRESS.set(len(_tasks))

    return task

@routes.get("", response_model=list[Task])
def list_tasks():
    """Return all tasks."""
    return list(_tasks.values())

@routes.get("/{task_id}", response_model=Task)
def get_task(task_id: int):
    """Fetch one task by ID."""
    if task_id not in _tasks:
        ERROR_COUNT.labels(error_type="task_not_found").inc()
        raise HTTPException(status_code=404, detail="Task not found")
    return _tasks[task_id]

@routes.patch("/{task_id}/complete", response_model=Task)
def complete_task(task_id: int):
    """Mark a task as done."""
    if task_id not in _tasks:
        ERROR_COUNT.labels(error_type="task_not_found").inc()
        raise HTTPException(status_code=404, detail="Task not found")

    _tasks[task_id]["done"] = True
    # Gauge stays the same here, but you could change it if "in progress" meant not done
    return _tasks[task_id]

@routes.delete("/{task_id}", status_code=204)
def delete_task(task_id: int):
    """Delete a task."""
    if task_id not in _tasks:
        ERROR_COUNT.labels(error_type="task_not_found").inc()
        raise HTTPException(status_code=404, detail="Task not found")

    del _tasks[task_id]
    TASKS_IN_PROGRESS.set(len(_tasks))
    return None