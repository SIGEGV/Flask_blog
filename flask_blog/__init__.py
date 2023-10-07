from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

# go to python cli and type improt secrets and then secrets.token_hex(16) and it will give you a randon 16 digit key value
app.config["SECRET_KEY"] = "b05103f9ee374fa043ba58ced99cfcb4"
#  setting up the config of the data base and then creating ur database class;
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "user.login"
login_manager.login_message_category = "info"
#  dont change its position done to prevent cyclecalling
from flask_blog.user.routes import users
from flask_blog.post.routes import posts
from flask_blog.main.routes import main 
from flask_blog.errors.handlers import errors
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main )
app.register_blueprint(errors)


# https://stackoverflow.com/questions/44941757/sqlalchemy-exc-operationalerror-sqlite3-operationalerror-no-such-table
from .models import User, Post

with app.app_context():
    db.create_all()
