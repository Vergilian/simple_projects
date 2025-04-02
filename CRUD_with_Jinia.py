from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int


@app.get("/")
def get_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get(path="/users/{user_id}", response_model=User)
def get_all_users(request: Request, user_id: int) -> HTMLResponse:
    user = next((u for u in users if u.id == user_id), None)
    if user is not None:
        return templates.TemplateResponse("users.html", {"request": request, "user": user})
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.post("/user", response_model=User)
def create_user(request:Request, username: str = Form(...), age: int= Form(...)) -> HTMLResponse:
    new_id = users[-1].id + 1 if users else 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.put("/user/{user_id}/{username}/{age}", response_model=User)
def update_users(user_id: int, username: str, age=int):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/user/{user_id}", response_model=User)
def delete_user(user_id: int):
    for index, user in enumerate(users):
        if user.id == user_id:
            return users.pop(index)
    raise HTTPException(status_code=404, detail="User not found")

# python -m uvicorn shablon:app
