# from application import db, app
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
# from application import routes

# Create a Flask Isntance
app = Flask(__name__)

# Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///income_expenseDB.db'

# Secret Key！
app.config['SECRET_KEY'] = 'my super secrect key'

# Initialize the database
db = SQLAlchemy(app)

# Create model
class add_expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(30),nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __init__(self,amount, category, date):
        self.amount = amount
        self.category = category
        self.date = date

with app.app_context():
    db.create_all()
        

class ExpenseForm(FlaskForm):
    amount = IntegerField('Amount', validators = [DataRequired()]) 
    category = SelectField ('Category', validators=[DataRequired()],
                                            choices =[('Rent', 'Rent'),
                                                      ('Food and Beverage','Food and Beverage'),
                                                      ('Shopping','Shopping'),
                                                      ('Transport','Transport')])
    date = DateField('Date', format='%Y-%m-%d', validators = [DataRequired()])
    submit = SubmitField('Save')

                                                
                                            




