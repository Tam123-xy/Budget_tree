from application import db, app

class add_expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Double, nullable=False)
    category = db.Column(db.String(30),nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(10), nullable=False, default= 'Expense')
    nota = db.Column(db.String(15))

    def __init__(self,amount, category, date, nota):
        self.amount = amount
        self.category = category
        self.date = date
        self.nota = nota

class add_incomes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Double, nullable=False)
    category = db.Column(db.String(30),nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(10), nullable=False, default= 'Income')
    nota = db.Column(db.String(15))

    def __init__(self,amount, category, date, nota):
        self.amount = amount
        self.category = category
        self.date = date
        self.nota = nota

IMAGES = [
    "../static/tree_images/tree1.png", # 0-33% progress
    "../static/tree_images/tree2.png", # 34-66% progress
    "../static/tree_images/tree3.png", # 67-99% progress
    "../static/tree_images/tree_goal.jpg" # 100% progress (goal achieved)
]

class goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Double, nullable=False)
    month = db.Column(db.String(30),nullable=False)
    year = db.Column(db.Integer, nullable=False)
    current_savings = db.Column(db.Float, default=0.0)
    image = db.Column(db.String(255), default=IMAGES[0])
    achieved = db.Column(db.Boolean, default=False)

    def __init__(self,amount,month,year):
        self.amount = amount
        self.month = month
        self.year = year

class net(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Double, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(10), nullable=False)
   
    def __init__(self,amount,date,type):
        self.amount = amount
        self.date = date
        self.type = type

class month_and_year(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
     
    def __init__(self,month,year):
        self.month = month
        self.year = year

with app.app_context():
    db.create_all()