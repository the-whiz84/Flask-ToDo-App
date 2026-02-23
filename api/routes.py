from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from .models import db, User, Task, TaskList
from .forms import RegisterForm, LoginForm, TaskForm, TaskListForm

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    return render_template("index.html")


@main_bp.route("/register", methods=["GET", "POST"])
def register():
    # If user comes here while logged in, redirect them
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
        
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        user = db.session.scalar(db.select(User).where(User.email == email))
        
        if user:
            flash("You've already signed up with that email, log in instead!", "warning")
            return redirect(url_for("main.login"))

        hashed_password = generate_password_hash(
            password=form.password.data, method="scrypt", salt_length=16
        )
        new_user = User(
            username=form.username.data,
            email=email,
            password=hashed_password,
        )
        db.session.add(new_user)
        db.session.commit()
        
        # Create a default list for new users
        default_list = TaskList(name="My Tasks", user_id=new_user.id)
        db.session.add(default_list)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for("main.home"))
        
    return render_template("register.html", form=form)


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(db.select(User).where(User.email == form.email.data))
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("main.home"))
        else:
            flash("Login unsuccessful. Please check email and password.", "danger")
            
    return render_template("login.html", form=form)


@main_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@main_bp.route("/home")
@login_required
def home():
    # Get all lists for sidebar
    user_lists = TaskList.query.filter_by(user_id=current_user.id).all()
    
    # If user has no lists (edge case since we create one on signup), create one
    if not user_lists:
        default_list = TaskList(name="My Tasks", user_id=current_user.id)
        db.session.add(default_list)
        db.session.commit()
        user_lists = [default_list]

    # Get active list ID from query arg, default to the first list
    list_id_str = request.args.get("list_id")
    active_list_id = int(list_id_str) if list_id_str and list_id_str.isdigit() else user_lists[0].id
    
    active_list = db.session.get(TaskList, active_list_id)
    # Ensure they own the list
    if not active_list or active_list.user_id != current_user.id:
        active_list = user_lists[0]
        
    tasks = Task.query.filter_by(task_list_id=active_list.id).order_by(Task.create_date.desc()).all()
    
    task_form = TaskForm()
    # Populate the dynamic choices for the list dropdown
    task_form.list_id.choices = [(tl.id, tl.name) for tl in user_lists]
    task_form.list_id.data = active_list.id # default selected option

    list_form = TaskListForm()

    return render_template(
        "home.html", 
        lists=user_lists, 
        active_list=active_list, 
        tasks=tasks, 
        task_form=task_form,
        list_form=list_form,
    )


@main_bp.route("/list/add", methods=["POST"])
@login_required
def add_list():
    form = TaskListForm()
    if form.validate_on_submit():
        new_list = TaskList(name=form.name.data, user_id=current_user.id)
        db.session.add(new_list)
        db.session.commit()
        flash("List created successfully.", "success")
        return redirect(url_for("main.home", list_id=new_list.id))
    
    flash("Error creating list.", "danger")
    return redirect(url_for("main.home"))
    
    
@main_bp.route("/list/delete/<int:list_id>", methods=["POST"])
@login_required
def delete_list(list_id):
    target_list = db.session.get(TaskList, list_id)
    if target_list and target_list.user_id == current_user.id:
        db.session.delete(target_list)
        db.session.commit()
        flash("List deleted.", "success")
    return redirect(url_for("main.home"))


@main_bp.route("/task/add", methods=["POST"])
@login_required
def add_task():
    form = TaskForm()
    # Refresh choices just in case
    user_lists = TaskList.query.filter_by(user_id=current_user.id).all()
    form.list_id.choices = [(tl.id, tl.name) for tl in user_lists]
    
    if form.validate_on_submit():
        # verify the selected list belongs to the user
        list_id = form.list_id.data
        if any(tl.id == list_id for tl in user_lists):
            new_task = Task(
                task=form.task.data,
                due_date=form.due_date.data,
                status="open",
                task_list_id=list_id
            )
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for("main.home", list_id=list_id))
            
    flash("Invalid data. Please try again.", "danger")
    return redirect(url_for("main.home"))


@main_bp.route("/task/update", methods=["POST"])
@login_required
def update_task():
    task_id = request.form.get("task_id")
    action = request.form.get("action") 
    
    # We join to task_list to ensure current user owns the list this task belongs to
    task = db.session.query(Task).join(TaskList).filter(Task.id == task_id, TaskList.user_id == current_user.id).first()
    
    if task:
        list_id = task.task_list_id
        if action == "complete":
            # Toggle complete status
            task.status = "complete" if task.status == "open" else "open"
        elif action == "delete":
            db.session.delete(task)
        elif action == "edit":
            # Optional: handle inline edit via modal
            new_text = request.form.get("task_text")
            new_date = request.form.get("due_date")
            if new_text and new_date:
                task.task = new_text
                try:
                    task.due_date = datetime.strptime(new_date, "%Y-%m-%d").date()
                except ValueError:
                    pass

        db.session.commit()
        return redirect(url_for("main.home", list_id=list_id))
        
    flash("Task update failed.", "danger")
    return redirect(url_for("main.home"))
