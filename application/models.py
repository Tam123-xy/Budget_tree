from . import db
from datetime import datetime

class IncomeExpense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type =db.Column(db.String, default='income', nullable=False)
    category =db.Column(db.String(30), nullable=False, default='rent')
    date = db.Column(db.DateTime, nullable= False, default= datetime.utcnow)
    amount =db.column(db.Integer, nullable= False)

    def __str__(self):
        return self.id