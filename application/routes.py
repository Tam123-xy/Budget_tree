from application import app , db
from flask import render_template, url_for, redirect,flash, get_flashed_messages
from application.form import ExpenseForm
from application.models import add_expenses


@app.route('/')
def index():
    entries = add_expenses.query.order_by(add_expenses.date.desc()).all()
    return render_template('index.html', title="index", entries= entries)

@app.route('/dashboard')
def piechart():
    return render_template('piechart.html', title="dashboard")


@app.route('/add', methods = ["POST", "GET"])
def add_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        entry = add_expenses(amount=form.amount.data, category=form.category.data, date=form.date.data)
        db.session.add(entry)
        db.session.commit()
        flash(f"RM{form.amount.data} has been added to expense record", "success")
        return redirect(url_for('index'))
    return render_template('add_expense.html', title="Add expenses", form=form)

@app.route('/delete/<int:entry_id>')
def delete(entry_id):
    entry = add_expenses.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    flash('Deletion was success', 'success')
    return redirect(url_for('index'))