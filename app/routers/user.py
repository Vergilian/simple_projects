from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db

from app.models import *
from app.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.execute(select(Users)).scalars().all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There are no users"
        )
    return users


@router.get("/user_id")
async def get_user_by_id(users_id: int, db: Annotated[Session, Depends(get_db)]):
    # Выполняем выборку пользователя по его ID
    user = db.scalar(select(Users).where(Users.id == users_id))

    # Если пользователь не найден - выбрасываем исключение 404
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found"
        )
    return user


@router.post("/create")
async def create_user(db: Annotated[Session, Depends(get_db)], create_user: CreateUser, user_id: int):
    # Проверка на существование пользователя по user_id или username
    existing_user = db.scalar(
        select(Users).where(
            (Users.id == user_id) |
            (Users.username == create_user.username)
        )
    )
    # Добавление нового пользователя
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this ID or username already exists"
        )

    db.execute(insert(Users).values(username=create_user.username,
                                    firstname=create_user.firstname,
                                    lastname=create_user.lastname,
                                    age=create_user.age,
                                    slug=slugify(create_user.lastname)))

    db.commit()
    return {
        "status_code": status.HTTP_201_CREATED,
        "transaction": "Successful"
    }


@router.put("/update")
async def update_user(users_id: int, db: Annotated[Session, Depends(get_db)], update_user: UpdateUser):
    user = db.scalar(select(Users).where(Users.id == users_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user was not found"
        )

    db.execute(update(Users).where(Users.id == users_id).values(
        firstname=update_user.firstname,
        lastname=update_user.lastname,
        age=update_user.age,
        slug=slugify(update_user.lastname)
        )
    )

    db.commit()
    return {
        "status_code": status.HTTP_200_OK,
        "transaction": "User update is successful!"
    }


@router.delete("/delete")
async def delete_user(db: Annotated[Session, Depends(get_db)], users_id: int):
    user = db.scalar(select(Users).where(Users.id == users_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user was not found"
        )
    # Удаление всех задач, связанных с этим пользователем
    db.execute(delete(Tasks).where(Tasks.user_id == users_id))
    # Деактивация пользователя
    db.execute(update(Users).where(Users.id == users_id).values(is_active=False))
    db.commit()
    return {
        "status_code": status.HTTP_200_OK,
        "transaction": "User delete is successful"
    }


@router.delete("/deleted_but_in_system")
async def delete_user(db: Annotated[Session, Depends(get_db)], users_id: int):
    # Ищем пользователя по users_id
    user = db.scalar(select(Users).where(Users.id == users_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user was not found"
        )

    # 1. Удаление всех задач, связанных с этим пользователем
    db.execute(delete(Tasks).where(Tasks.user_id == users_id))
    db.commit()  # Сохраняем изменения после удаления задач

    # 2. Удаление самого пользователя
    db.delete(user)
    db.commit()  # Сохраняем изменения после удаления пользователя

    return {
        "status_code": status.HTTP_200_OK,
        "transaction": "User and related tasks have been completely deleted"
    }