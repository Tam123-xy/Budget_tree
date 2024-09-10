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

class goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Double, nullable=False)
    month = db.Column(db.String(30),nullable=False)
   
    def __init__(self,amount,month):
        self.amount = amount
        self.month = month


with app.app_context():
    db.create_all()