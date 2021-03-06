
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from recipe_app.config import Config
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os
# APPSETUP
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.urandom(24)
# DBSETUP
db = SQLAlchemy(app)
# LOGINSETUP
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from .models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


bcrypt = Bcrypt(app)
# REGESTERING BLUEPRINTS
from recipe_app.auth.routes import auth as auth_routes
from recipe_app.main import modify_routes, view_routes, misc_routes

app.register_blueprint(modify_routes)
app.register_blueprint(view_routes)
app.register_blueprint(misc_routes)
app.register_blueprint(auth_routes)

# CREATING DATABASE
with app.app_context():
    db.create_all()
