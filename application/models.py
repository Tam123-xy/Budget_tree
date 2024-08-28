from application import db, app

class add_expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(30),nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(30), nullable=False, default= 'Expense')

    def __init__(self,amount, category, date):
        self.amount = amount
        self.category = category
        self.date = date

class add_incomes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(30),nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(30), nullable=False, default= 'Income')

    def __init__(self,amount, category, date):
        self.amount = amount
        self.category = category
        self.date = date

with app.app_context():
    db.create_all()