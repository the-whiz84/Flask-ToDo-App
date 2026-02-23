from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from .models import db, User
from .routes import main_bp
from .config import Config

bootstrap = Bootstrap5()
login_manager = LoginManager()
csrf = CSRFProtect()

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Configure login manager
    login_manager.login_view = "main.login"
    login_manager.login_message_category = "info"

    with app.app_context():
        db.create_all()

    # Register blueprints
    app.register_blueprint(main_bp)

    return app
