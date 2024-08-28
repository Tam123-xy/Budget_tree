from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = "key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///income_expenseDB.db'

db = SQLAlchemy(app)

from application import routes
