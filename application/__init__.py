from flask import Flask
# from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = "root"
# app.config['MYSQL_PASSWORD'] = ""
# app.config['MYSQL_DB'] = "budget_tree"


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recordDB.db'
# mysql = MySQL(app)
db = SQLAlchemy(app)

from application import routes
