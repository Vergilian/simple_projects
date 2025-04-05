from app.backend.db import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = "users"
    __table_args__ = {'keep_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    is_active = Column(Boolean, default=True)
    age = Column(Integer)
    slug = Column(String, unique=True, index=True)
    tasks = relationship('Tasks', back_populates='user')


def print_tables():
    from app.models.task import Tasks  # Отложенный импорт Category
    from sqlalchemy.schema import CreateTable

    print(CreateTable(Users.__table__))
    print(CreateTable(Tasks.__table__))


if __name__ == "__main__":
    print_tables()
# меня интересует user_id св3язанные с users.id