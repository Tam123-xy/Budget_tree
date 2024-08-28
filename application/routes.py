from application.models import app, db
from flask import render_template, flash, redirect, url_for, get_flashed_messages
from application.models import ExpenseForm, add_expenses
from flask_sqlalchemy import SQLAlchemy


@app.route('/')
def index():
    return render_template('index.html', title = 'index')
 
@app.route('/dashboard')
def piechart():
    return render_template('piechart.html', title = 'dashboard')

@app.route('/add', methods =['GET','POST'])
def add_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        if True:
                entry = add_expenses(amount=form.amount.data, category=form.category.data, date=form.date.data)
                db.session.add(entry)
                db.session.commit()
                amount = form.amount.data
        # form.amount.data = ''
        # form.category.data = ''
        # form.date.data = ''
        flash(f"RM{amount} has been added to expense record", "success")
        # the_expense = add_expenses.query.order(add_expenses.id)
        return redirect(url_for('index'))
        
    return render_template('add_expense.html', title="Add expenses", form=form)
        
@app.route("/dashboard")
def dashboard():
     
    return render_template("dashboard.html")