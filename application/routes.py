from application import app , db
from flask import render_template, url_for, redirect,flash, get_flashed_messages
from application.form import ExpenseForm, IncomeForm
from application.models import add_expenses, add_incomes


# @app.route('/')
# def index():
#     entries = add_expenses.query.order_by(add_expenses.date.desc()).all()
#     return render_template('index.html', title="index", entries= entries)

@app.route('/')
def index():
    # Querying both models
    expenses = add_expenses.query.order_by(add_expenses.date.desc()).all()
    incomes = add_incomes.query.order_by(add_incomes.date.desc()).all()

    # Combine the entries
    entries = []
    
    # Add expenses to the combined list
    for expense in expenses:
        entries.append({
            'id': expense.id,
            'date': expense.date,
            'type': 'Expense',
            'category': expense.category,  # Assuming a category field exists
            'amount': expense.amount
        })
    
    # Add incomes to the combined list
    for income in incomes:
        entries.append({
            'id': income.id,
            'date': income.date,
            'type': 'Income',
            'category': income.category,  # Assuming the source acts as a category
            'amount': income.amount
        })

    # Sort the combined list by date in descending order
    entries.sort(key=lambda x: x['date'], reverse=True)

    return render_template('index.html', title="index", entries=entries)


@app.route('/dashboard')
def piechart():
    return render_template('piechart.html', title="dashboard")


@app.route('/addexpense', methods = ["POST", "GET"])
def add_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        entry = add_expenses(amount=form.amount.data, category=form.category.data, date=form.date.data)
        db.session.add(entry)
        db.session.commit()
        flash(f"RM{form.amount.data} has been added to expense record", "success")
        return redirect(url_for('index'))
    return render_template('add_expense.html', title="Add expenses", form=form)

@app.route('/addincome', methods = ["POST", "GET"])
def add_income():
    form = IncomeForm()
    if form.validate_on_submit():
        entry = add_incomes(amount=form.amount.data, category=form.category.data, date=form.date.data)
        db.session.add(entry)
        db.session.commit()
        flash(f"RM{form.amount.data} has been added to expense record", "success")
        return redirect(url_for('index'))
    return render_template('add_income.html', title="Add expenses", form=form)


@app.route('/delete/<int:entry_id>')
def delete(entry_id):
    if type == 'expense':
        entry = add_expenses.query.get_or_404(entry_id) 
        
    else:
        entry = add_incomes.query.get_or_404(entry_id) 
    
    db.session.delete(entry)
    db.session.commit()
    flash('Deletion was success', 'success')
    return redirect(url_for('index'))