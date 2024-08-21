from application import app, db
from flask import render_template, flash, redirect, url_for, get_flashed_messages
from application.form import UserDataForm
# from flask_mysqldb import MySQL
from application.models import IncomeExpenses

@app.route('/')
def index():
    return render_template('index.html', title = 'index')

# @app.route('/add', methods =['GET','POST'])
# def add_expense():
#     form= UserDataForm()
#     if form.validate_on_submit():
#         amount=form.amount.data
#         category= form.category.data
#         type= form.type.data 

#         db.session.add(entry)
#         db.session.commit()
#         flash('Successful entry','success')
#         return(url_for('index'))

@app.route('/add', methods =['GET','POST'])
def Expense2():
    return render_template('Expense2.html')
    form= UserDataForm()
    if form.validate_on_submit():
        amount=form.amount.data
        category= form.category.data
        type= form.type.data 

        db.session.add(entry)
        db.session.commit()
        flash('Successful entry','success')
        return(url_for('index'))

    if form.validate_on_submit():
        print(f"Amount: {form.amount.data}, Type: {form.type.data}, Category: {form.category.data}")
    # Then proceed with creating the entry

    return render_template('add.html', title = 'layout', form= form)

