from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db

from app.models import *
from app.schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/")
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.execute(select(Tasks)).scalars().all()
    if tasks is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There are no tasks"
        )
    return tasks


@router.get("/task_id")
async def get_task_by_id(task_id: int, db: Annotated[Session, Depends(get_db)]):
    # Выполняем выборку задачи по её ID
    task = db.scalar(select(Tasks).where(Tasks.id == task_id))

    # Если задача не найдена - выбрасываем исключение 404
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task was not found"
        )
    return task

@router.get("/user_id/tasks")
async def tasks_by_user_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.scalar(select(Users).where(Users.id == user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    tasks = db.execute(select(Tasks).where(Tasks.user_id == user_id)).scalars().all()
    return tasks

@router.post("/create")
async def create_task(db: Annotated[Session, Depends(get_db)], create_task: CreateTask, user_id: int):
    # Проверка существует ли пользователь
    user = db.scalar(select(Users).where(Users.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found"
        )

    db.execute(insert(Tasks).values(title=create_task.title,
                                   description=create_task.description,
                                   priority=create_task.priority,
                                   slug=slugify(create_task.title),
                                   user_id=user_id)) # связываем задачу с пользователем

    db.commit()
    return {
        "status_code": status.HTTP_201_CREATED,
        "transaction": "Successful"
    }


@router.put("/update")
async def update_task(task_id: int, db: Annotated[Session, Depends(get_db)], update_task: UpdateTask):
    task_update = db.scalar(select(Tasks).where(Tasks.id == task_id))
    if task_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user was not found"
        )

    db.execute(update(Tasks).where(Tasks.id == task_id).values(
        title=update_task.title,
        description=update_task.description,
        priority=update_task.priority,
        slug=slugify(update_task.title)
    ))

    db.commit()
    return {
        "status_code": status.HTTP_200_OK,
        "transaction": "Successful"
    }


@router.delete("/delete")
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    task_delete = db.scalar(select(Tasks).where(Tasks.id == task_id))
    if task_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The task was not found"
        )
    db.execute(update(Tasks).where(Tasks.id == task_id).values(completed=True))
    db.commit()
    return {
        "status_code": status.HTTP_200_OK,
        "transaction": "Task delete is successful"
    }


@router.delete("/delete/permanent/{task_id}")
async def permanent_delete_task(task_id: int, db: Annotated[Session, Depends(get_db)]):
    # Поиск задачи по ID
    task_to_delete = db.scalar(select(Tasks).where(Tasks.id == task_id))

    # Проверка существования задачи
    if task_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The task was not found"
        )

    # Полное удаление задачи
    db.execute(delete(Tasks).where(Tasks.id == task_id))
    db.commit()

    return {
        "status_code": status.HTTP_200_OK,
        "transaction": "Task deleted successfully"
    }