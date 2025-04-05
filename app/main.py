from fastapi import FastAPI
from app.routers import user, task

app = FastAPI()


@app.get("/")
async def welcome() -> dict:
    return {"message": "My taskmanager app"}


app.include_router(user.router)
app.include_router(task.router)

# python -m uvicorn app.main:app --reload
# alembic -c alembic_first.ini revision --autogenerate -m "Initial migration"
# alembic -c alembic_first.ini upgrade head