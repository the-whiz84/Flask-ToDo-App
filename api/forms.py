from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, DateField, SelectField
from wtforms.validators import DataRequired, Email, Length


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=64)])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, message="Password must be at least 8 characters long.")])
    submit = SubmitField("Sign Me Up")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class TaskListForm(FlaskForm):
    name = StringField("List Name", validators=[DataRequired(), Length(min=1, max=100)])
    submit = SubmitField("Create List")


class TaskForm(FlaskForm):
    task = StringField("Task Description", validators=[DataRequired(), Length(min=1, max=250)])
    due_date = DateField("Due Date", validators=[DataRequired()])
    # Optional field if we need to let user pick list from form, else assigned automatically by route
    list_id = SelectField("List", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Add Task")
