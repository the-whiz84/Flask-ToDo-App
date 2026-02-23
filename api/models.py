from datetime import date, datetime
from flask_login import UserMixin
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, func, ForeignKey
from flask_sqlalchemy import SQLAlchemy

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(250))
    lists: Mapped[list["TaskList"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class TaskList(db.Model):
    __tablename__ = "task_lists"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="lists")
    tasks: Mapped[list["Task"]] = relationship(back_populates="task_list", cascade="all, delete-orphan", order_by="Task.create_date")


class Task(db.Model):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task: Mapped[str] = mapped_column(String(250), nullable=False)
    create_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    due_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    
    task_list_id: Mapped[int] = mapped_column(ForeignKey("task_lists.id"))
    task_list: Mapped["TaskList"] = relationship(back_populates="tasks")

    @property
    def due_status(self):
        today = date.today()
        # handle naive vs aware datetimes based on how it was saved
        due_date_obj = self.due_date.date() if isinstance(self.due_date, datetime) else self.due_date
        
        if due_date_obj == today:
            return "Due today"
        elif due_date_obj > today:
            return "On time"
        else:
            return "Past due"
