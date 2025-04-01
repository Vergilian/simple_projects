from fastapi import FastAPI, HTTPException

app = FastAPI()

users = {'1': "Имя: Example, возраст:18"}


@app.get("/")
async def read_root():
    return {"message": "Welcome to the API!"}


@app.get('/users')
async def get_all_users() -> dict:
    return users


@app.post("/user/{username}/{age}")
async def create_user(username: str, age: int) -> str:
    current_user_id = str(int(max(users.keys(), key=int)) + 1) if users else "1"
    users[current_user_id] = f"Имя: {username}, возраст: {age}"
    return f"User {username} is registered!"


@app.put("/user/{user_id}/{username}/{age}")
async def update_users(user_id: int, username: str, age: int) -> str:
    if user_id in users:
        users[user_id] = f"Имя: {username}, возраст: {age}"
        return f"user {user_id} id updated!"
    else:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

@app.delete("/user/{user_id}")
async def delete_user(user_id: int):
    for i, user in enumerate(users):
        if user["id"] == user_id:
            del user[i]
            return {"detail": "Пользователь удален"}
    raise HTTPException(status_code=404, detail="Пользователь не найдена")
