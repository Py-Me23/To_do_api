# Create a to do list
# add todo
# get all todos
# get single todo
# delete todo
# upadate todo


from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

task_db = {
    "church": {
        "tasktodo": "Prepare communion wine",
        "date_done": "2026-10-23",
        "location": "New Jersey",
    },
    "work": {
        "tasktodo": "Prepare files",
        "date_done": "2025-10-01",
        "location": "London",
    },
    "home": {
        "tasktodo": "Bath the kids",
        "date_done": "2027-10-14",
        "location": "New York",
    },
}


class Task(BaseModel):
    tasktodo: str = Field(min_length=3, max_length=20)
    date_done: date
    location: str


class TaskUpdate(Task):
    location: Optional[str] = None


app = FastAPI()


@app.get("/")
def my_intro():
    return {"messsage": "Welcome to my API tutorial on tasks"}


@app.get("/tasks")
def get_tasks():
    task_list = list(task_db.values())
    return task_list


@app.get("/tasks/{tasktodo}")
def get_tasks_path(tasktodo: str):
    return task_db[tasktodo]


@app.post("/tasks")
def create_task(task: Task):
    tasktodo = task.tasktodo
    task_db[tasktodo] = task.dict()
    return {"message": f"Sucessfully created task:{tasktodo}"}


@app.delete("/tasks/{tasktodo}")
def delete_task(tasktodo: str):
    del task_db[tasktodo]
    return {"message": f"Successfully deleted task: {tasktodo}"}


# @app.put("/tasks")
# def update_user(task: Task):
#     tasktodo = task.tasktodo
#     task_db[tasktodo] = task.dict()
#     return {"message": f"Sucessfully updated task:{tasktodo}"}


@app.patch("/tasks")
def update_task_partial(task: TaskUpdate):
    tasktodo = task.tasktodo
    task_db[tasktodo].update(task.dict(exclude_unset=True))
    # print("successfully updated")
    return {"message": f"Sucessfully updated task:{tasktodo}"}
