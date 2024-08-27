from application import db, app
import enum

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