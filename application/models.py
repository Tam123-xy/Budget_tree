from application import db, app
from datetime import datetime

class IncomeExpenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(30), default='Rent',nullable=False)
    type = db.Column(db.String(30), default = 'Income', nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self,amount,type,category):
        self.type= amount
        self.type= type
        self.type= category

with app.app_context():
    db.create_all()
    db.session.add(IncomeExpenses(amount = 2500, category ='Income',type= 'Salary'))
    db.session.add(IncomeExpenses(amount =330, category ='Expense', type='Rent'))
    db.session.add(IncomeExpenses(amount =200,category ='Expense', type= 'Grocery'))


