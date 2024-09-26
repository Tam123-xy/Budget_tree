from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)

bcrypt= Bcrypt(app)

app.config['SECRET_KEY'] = "key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///income_expenseDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)







from application import routes
