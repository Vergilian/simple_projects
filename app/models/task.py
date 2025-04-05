from app.backend.db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class Tasks(Base):
    __tablename__ = "tasks"
    __table_args__ = {"keep_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer,default=0)
    completed = Column(Boolean,default=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False ,index=True)
    slug = Column(String, unique=True, index=True)
    user = relationship('Users', back_populates='tasks')



def print_tables():
    # Отложенный импорт для предотвращения циклического импорта
    from app.models.user import Users
    from sqlalchemy.schema import CreateTable

    print(CreateTable(Users.__table__))
    print(CreateTable(Tasks.__table__))

if __name__ == "__main__":
    print_tables()