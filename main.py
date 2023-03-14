from deta import Base
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel  # pylint: disable=no-name-in-module
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
# Connect to a Base for storing todo items.
todos_base = Base("todos")


@app.get("/")
async def index():
    with open("./static/index.html") as file:
        return HTMLResponse(file.read())

@app.get("/login")
async def login():
    with open("./static/login.html") as file:
        return HTMLResponse(file.read())


@app.get("/api/todos")
async def get_todos_htmx():
    # Fetch all items from the Base.
    todos = todos_base.fetch()
    # Return the items as HTML list.
    todos_html = ""
    for item in todos.items:
        key, text = item["key"], item["text"]
        todos_html += f'<li id="{key}" hx-delete="/api/todos/{key}" hx-swap="delete" hx-trigger="click">{text}</li>'

    response = todos_html
    return HTMLResponse(response)


@app.post("/api/todos", status_code=201)
async def add_todo_htmx(text: str = Form()):
    print(text)
    # Put the item into the Base.
    resp = todos_base.put({"text": text})
    # Replace button.
    todo_input = """<input
      id="todo-input"
      type="text"
      name="text"
      hx-post="/api/todos"
      hx-trigger="keyup changed delay:500ms"
      hx-swap-oob="true"
      placeholder="Add another todo..."
    />"""
    return HTMLResponse(todo_input, headers={"HX-Trigger": "new-todo"})


@app.delete("/api/todos/{id}")
async def delete_todos_htmx(id: str):
    # Fetch all items from the Base.
    response = todos_base.delete(key=id)
    return response
