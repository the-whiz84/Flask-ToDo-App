import os
from datetime import date, datetime
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, func
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm

SQLALCHEMY_DATABASE_URI = os.getenv("POSTGRES_URL")


def due_status(due_date):
    today = date.today()
    due_date_obj = datetime.strptime(due_date, "%Y-%m-%d").date()
    if due_date_obj == today:
        return "Due today"
    elif due_date_obj > today:
        return "On time"
    elif due_date_obj < today:
        return "Past due"


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
bootstrap = Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config["SQLALCHEMY_DATABASE_URI"] = f"{SQLALCHEMY_DATABASE_URI}, sqlite:///todo.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLES
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(250))
    tasks: Mapped[list["Task"]] = relationship(back_populates="user")


class Task(db.Model):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task: Mapped[str] = mapped_column(String(250), nullable=False)
    create_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    due_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    due_status: Mapped[str] = mapped_column(String(50), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="tasks")


with app.app_context():
    db.create_all()


# Routes for the Todo App
@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    return render_template("index.html")


@app.route("/home")
@login_required
def home():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    username = current_user.username
    return render_template("home.html", todos=tasks, username=username)


# Existing routes for the Blog website
@app.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        email = register_form.email.data
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()
        if user:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for("login"))
        else:
            hashed_password = generate_password_hash(
                password=register_form.password.data, method="scrypt", salt_length=16
            )
            new_user = User(
                username=register_form.username.data,
                email=email,
                password=hashed_password,
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("home"))
    return render_template("register.html", form=register_form)


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("home"))
        else:
            flash("Login unsuccessful. Please check email and password.")
    return render_template("login.html", form=login_form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/add_task", methods=["POST"])
@login_required
def add_task():
    task = request.form.get("task")
    due_date_str = request.form.get("due_date")
    due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
    status = "open"
    due_status_value = due_status(due_date_str)
    new_task = Task(
        task=task,
        due_date=due_date,
        status=status,
        due_status=due_status_value,
        user_id=current_user.id,
    )
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/update_todo/", methods=["POST"])
@login_required
def update_todo():
    task_id = request.form.get("task_id")
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if task:
        button_pushed = request.form.get("update_todo")
        if button_pushed == "update":
            due_date_str = request.form.get("due_date")
            task.due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
            task.task = request.form.get("task")
        elif button_pushed == "complete":
            task.status = "complete"
        elif button_pushed == "delete":
            db.session.delete(task)
        db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run()
