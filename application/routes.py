from application import app , db
from flask import render_template, url_for, redirect,flash, request
from application.form import ExpenseForm, IncomeForm
from application.models import add_expenses, add_incomes
import json


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
            'type': expense.type,
            'category': expense.category,  # Assuming a category field exists
            'amount': expense.amount,
            'nota': expense.nota
        })
    
    # Add incomes to the combined list
    for income in incomes:
        entries.append({
            'id': income.id,
            'date': income.date,
            'type': income.type,
            'category': income.category,  # Assuming the source acts as a category
            'amount': income.amount,
            'nota': income.nota
        })

    # Sort the combined list by date in descending order
    entries.sort(key=lambda x: x['date'], reverse=True)

    # Get the total expenses
    sum_expenses = db.session.query(db.func.sum(add_expenses.amount)).all()
    sum_expense = [expense[0] if expense[0] is not None else 0 for expense in sum_expenses]

    # Get the total incomes
    sum_incomes = db.session.query(db.func.sum(add_incomes.amount)).all()
    sum_income = [income[0] if income[0] is not None else 0 for income in sum_incomes]

    net = [round(sum_income[0] - sum_expense[0], 2)]

    return render_template('index.html', title="Transaction history", entries=entries,  sum_expense=sum_expense, sum_income=sum_income, net=net)

@app.route('/default_table')
def default_table():
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
            'type': expense.type,
            'category': expense.category,  # Assuming a category field exists
            'amount': expense.amount,
            'nota': expense.nota
        })
    
    # Add incomes to the combined list
    for income in incomes:
        entries.append({
            'id': income.id,
            'date': income.date,
            'type': income.type,
            'category': income.category,  # Assuming the source acts as a category
            'amount': income.amount,
            'nota': income.nota
        })

    # Sort the combined list by date in descending order
    entries.sort(key=lambda x: x['date'], reverse=True)

    return render_template('default_table.html', entries=entries)


@app.route('/addexpense', methods = ["POST", "GET"])
def add_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        entry = add_expenses(amount=form.amount.data, category=form.category.data, date=form.date.data, nota=form.nota.data)
        db.session.add(entry)
        db.session.commit()
        flash(f"RM{form.amount.data} has been added to expense record", "success")
        return redirect(url_for('index'))
    
    expenses = add_expenses.query.order_by(add_expenses.date.desc()).all()
    
    return render_template('add_expense.html', title="Add expense", form=form, expenses=expenses )
    
 
@app.route('/addincome', methods = ["POST", "GET"])
def add_income():
    form = IncomeForm()
    if form.validate_on_submit():
        entry = add_incomes(amount=form.amount.data, category=form.category.data, date=form.date.data,  nota=form.nota.data)
        db.session.add(entry)
        db.session.commit()
        flash(f"RM{form.amount.data} has been added to expense record", "success")
        return redirect(url_for('index'))
    
    incomes = add_incomes.query.order_by(add_incomes.date.desc()).all()
    
    return render_template('add_income.html', title="Add income", form=form, incomes=incomes)


@app.route('/delete/<int:entry_id>/<string:entry_type>', methods=['POST', 'GET'])
def delete(entry_id, entry_type):
    if entry_type == 'Expense':
        entry = add_expenses.query.get_or_404(entry_id) 
        
    else:
        entry = add_incomes.query.get_or_404(entry_id) 
    
    db.session.delete(entry)
    db.session.commit()
    flash('Deletion was success', 'success')

    # Determine the page to return to, with a fallback to 'index'
    next_page = request.args.get('next') 
    
    # Redirect to the specified page
    return redirect(next_page)


@app.route('/dashboard')
def dashboard():

    # piechart
    expenses = db.session.query(db.func.sum(add_expenses.amount)).all()
    expense = [total_expense[0] for total_expense in expenses]

    incomes = db.session.query(db.func.sum(add_incomes.amount)).all()
    income = [total_income[0] for total_income in incomes]

    # linechart
    dates = db.session.query(db.func.sum(add_expenses.amount), add_expenses.date).group_by(add_expenses.date).order_by(add_expenses.date).all()
    over_time_expenditure = []
    dates_labels = []
    for amount, date in dates:
        over_time_expenditure.append(amount)
        dates_labels.append(date.strftime('%d-%m-%Y'))

    dates_incomes = db.session.query(db.func.sum(add_incomes.amount), add_incomes.date).group_by(add_incomes.date).order_by(add_incomes.date).all()
    over_time_expenditure_income = []
    dates_income_labels = []
    for amount, date in dates_incomes:
        over_time_expenditure_income.append(amount)
        dates_income_labels.append(date.strftime('%d-%m-%Y'))

    # barchart
    income_category_amount = db.session.query(add_incomes.category, db.func.sum(add_incomes.amount)).group_by(add_incomes.category).all()

    income_category_amounts = []
    income_categorys = []
    
    for category, amount in income_category_amount:
        income_category_amounts.append(amount)
        income_categorys.append(category)

    
    return render_template('dashboard.html', title="Dashboard", 
                           sum_expenses = json.dumps(expense), 
                           sum_incomes = json.dumps(income), 
                           over_time_expenditure =json.dumps(over_time_expenditure),
                           dates_label = json.dumps(dates_labels),
                           over_time_income =json.dumps(over_time_expenditure_income),
                           dates_income = json.dumps(dates_income_labels),
                           income_category_amount = json.dumps(income_category_amounts),
                           income_category = json.dumps(income_categorys)
                           )

@app.route('/search')
def search():
    q = request.args.get('q')
    print(q)
    
    if q:
        results = db.session.query(add_expenses).filter(add_expenses.nota.icontains(q) | add_expenses.amount.icontains(q) | add_expenses.date.icontains(q)| add_expenses.category.icontains(q)).order_by(add_expenses.date.asc()).all()

    else:
        results = []

    return render_template('search_result.html', results=results)

    

@app.route('/tree', methods=['POST', 'GET'])
def tree():
#         image_list = [
#         'tree1.png',
#         'tree2.png',
#         'tree3.png',
#         'tree4.png',
#         'tree5.png',
#         'tree6.png',
#         'tree7.png',
#         'tree8.png',
#         'tree9.png'
#     ]

# def show_previous_image(self):
#     if self.current_image_index > 0 :
#         self.current_image_index -= 1
#     else:
#         self.current_image_index = len(self.image_labels) - 1 :
#         self.image_label.config(image=self.image_;abels[self.current_image_index])

# def show_next_image(self):
#     if self.current_image_index < len(self.image_labels) - 1 :
#        self.current_image_index += 1
#     else:
#         self.current_image_index = 0
#     self.image_label.config(image=self.image_labels[self.current_image_index])
    return render_template('tree.html', title="tree")


 #transactions = Transactions.query.filter(Transactions.date_posted > date.today() - timedelta(weeks=1)).all()

 #transactions = Transactions.query.filter(Transactions.datetime_posted > datetime.now() - timedelta(days=30)).all()

# transactions = db.session.query(Transactions.date_posted, func.sum(Transactions.amount)).group_by(Transactions.date_posted).all()

#transactions = db.session.query(func.strftime('%Y', Transactions.date_posted), func.sum(Transactions.amount)).group_by(func.strftime('%Y', Transactions.date_posted)).all()


