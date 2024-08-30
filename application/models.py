from application import db, app

class add_expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(30),nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(30), nullable=False, default= 'Expense')
    nota = db.Column(db.String(15))

    def __init__(self,amount, category, date, nota):
        self.amount = amount
        self.category = category
        self.date = date
        self.nota = nota

class add_incomes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(30),nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(30), nullable=False, default= 'Income')
    nota = db.Column(db.String(15))

    def __init__(self,amount, category, date, nota):
        self.amount = amount
        self.category = category
        self.date = date
        self.nota = nota

with app.app_context():
    db.create_all()