from application import db, app
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    expenses = db.relationship('add_expenses', backref='user', lazy=True)
    incomes = db.relationship('add_incomes', backref='user', lazy=True)
    net = db.relationship('net', backref='user', lazy=True)
    category = db.relationship('category', backref='user', lazy=True)
    goal = db.relationship('goal', backref='user', lazy=True)

class add_expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Double, nullable=False)
    category = db.Column(db.String(30),nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(10), nullable=False, default= 'Expense')
    nota = db.Column(db.String(15))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 

    def __init__(self,amount, category, date, nota, user_id):
        self.amount = amount
        self.category = category
        self.date = date
        self.nota = nota
        self.user_id = user_id

class add_incomes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Double, nullable=False)
    category = db.Column(db.String(30),nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(10), nullable=False, default= 'Income')
    nota = db.Column(db.String(15))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 

    def __init__(self,amount, category, date, nota, user_id):
        self.amount = amount
        self.category = category
        self.date = date
        self.nota = nota
        self.user_id = user_id

class goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Double, nullable=False)
    month = db.Column(db.String(30),nullable=False)
    year = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 

    def __init__(self,amount,month,year, user_id):
        self.amount = amount
        self.month = month
        self.year = year
        self.user_id = user_id

class net(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Double, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
   
    def __init__(self,amount,date,type, user_id):
        self.amount = amount
        self.date = date
        self.type = type
        self.user_id = user_id

class category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
     
    def __init__(self,type,category, user_id):
        self.type = type
        self.category = category
        self.user_id = user_id

with app.app_context():
    db.create_all()