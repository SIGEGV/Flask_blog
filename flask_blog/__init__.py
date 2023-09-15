from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)

# go to python cli and type improt secrets and then secrets.token_hex(16) and it will give you a randon 16 digit key value
app.config['SECRET_KEY']='b05103f9ee374fa043ba58ced99cfcb4'


#  setting up the config of the data base and then creating ur database class;
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
db=SQLAlchemy(app)

#  dont change its position done to prevent cyclecalling
from flask_blog import routes