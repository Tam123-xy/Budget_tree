from application import app , db
from flask import render_template, url_for, redirect,flash, request
from application.form import ExpenseForm, IncomeForm, GoalForm, create_categoryForm
from application.models import add_expenses, add_incomes, goal, net, category
from sqlalchemy import func, case, and_
import json
from datetime import datetime, date, timedelta
from sqlalchemy.sql import text
from decimal import Decimal

def combine_table(expenses,incomes):
    # Combine the entries
    entries = []
    
    # after query add_expenses model, put in 'expenses' variable, 'expenses' is appended into entries list
    for expense in expenses:
        entries.append({
            'id': expense.id,
            'date': expense.date,
            'type': expense.type,
            'category': expense.category, 
            'amount': expense.amount,
            'nota': expense.nota
        })
    
    # after query add_incomes model, put in 'incomes' variable, 'incomes' is appended into entries list
    for income in incomes:
        entries.append({
            'id': income.id,
            'date': income.date,
            'type': income.type,
            'category': income.category,
            'amount': income.amount,
            'nota': income.nota
        })

    # Sort the combined list by date in descending order
    entries.sort(key=lambda x: x['date'], reverse=True)
    return entries

def goal_net(net_query,goall):
     # Create a dictionary for net results with 'month_year' as key
    net_dict = {result.month_year: result.total for result in net_query}

    amounts = []

    # Loop through each goal entry and compare with the net data
    for goal_entry in goall:
        # Create the formatted 'year-month' string for the goal entry
        month_year = f'{goal_entry.year}-{int(goal_entry.month):02d}'

        # Get the net amount if the month_year exists in net_dict, otherwise set net to 0
        net_amount = net_dict.get(month_year, 0)

        if goal_entry.amount == 0 :
            progress = 0

        else:  # Avoid division by zero
            progress = ( net_amount / goal_entry.amount) * 100
            progress = min(progress, 100)  # Cap progress at 100%

        # Append the results
        amounts.append({
            'id':goal_entry.id,
            'month_year': month_year,
            'goal': goal_entry.amount,
            'net': net_amount,
            'progress' :progress
        })

    amounts.sort(key=lambda x: x['month_year'], reverse=True)
    return amounts


@app.route('/', methods = ["POST", "GET"])
def index():
   
    # Querying both models
    expenses = add_expenses.query.order_by(add_expenses.date.desc()).all()
    incomes = add_incomes.query.order_by(add_incomes.date.desc()).all()

    # Combine the results of query 
    entries = combine_table(expenses,incomes)

    # Get the total expenses
    sum_expenses = db.session.query(db.func.sum(add_expenses.amount)).all()
    sum_expense = [expense[0] if expense[0] is not None else 0 for expense in sum_expenses]

    # Get the total incomes
    sum_incomes = db.session.query(db.func.sum(add_incomes.amount)).all()
    sum_income = [income[0] if income[0] is not None else 0 for income in sum_incomes]

    # Count the net saving
    net = [round(sum_income[0] - sum_expense[0], 2)]

    return render_template('index.html', title="Transaction history", entries=entries,  sum_expense=sum_expense, sum_income=sum_income, net=net)

@app.route('/set', methods=['POST','GET'])
def set():
    month = request.form.get('month')
    year = request.form.get('year')
   
    current_year_month = f'{year}-{int(month):02d}'
   
    expenses = add_expenses.query.filter(func.strftime('%Y-%m', add_expenses.date) == current_year_month).all()
    incomes = add_incomes.query.filter(func.strftime('%Y-%m', add_incomes.date) == current_year_month).all()
    entries = combine_table(expenses,incomes)
    return render_template('default_table.html',entries=entries)

@app.route('/set_income', methods=['POST','GET'])
def set_income():

    # Get the month and year which are setted by user 
    month = request.form.get('month')
    year = request.form.get('year')
   
    # year-month format
    current_year_month = f'{year}-{int(month):02d}'

    # Query add_incomes models with the condition of the year-month
    incomes = add_incomes.query.filter(func.strftime('%Y-%m', add_incomes.date) == current_year_month).all()
    incomes.sort(key=lambda x: x.date, reverse=True)

    return render_template('default_table_income.html',incomes=incomes)

@app.route('/set_expense', methods=['POST','GET'])
def set_expense():
    # Get the month and year which are setted by user, transfer into year-month format
    month = request.form.get('month')
    year = request.form.get('year')
    current_year_month = f'{year}-{int(month):02d}'

   # Query add_incomes models with the condition of the year-month, sort it by date in descending order
    expenses = add_expenses.query.filter(func.strftime('%Y-%m', add_expenses.date) == current_year_month).all()
    expenses.sort(key=lambda x: x.date, reverse=True)

    return render_template('default_table_expense.html',expenses=expenses)

@app.route('/net_all_table')
def net_all_table():

    # Get the total expenses
    sum_expenses = db.session.query(db.func.sum(add_expenses.amount)).all()
    sum_expense = [expense[0] if expense[0] is not None else 0 for expense in sum_expenses]

    # Get the total incomes
    sum_incomes = db.session.query(db.func.sum(add_incomes.amount)).all()
    sum_income = [income[0] if income[0] is not None else 0 for income in sum_incomes]

    # Count the net saving
    net = [round(sum_income[0] - sum_expense[0], 2)]

    return render_template('net_all_table.html', sum_expense=sum_expense, sum_income=sum_income, net=net)

@app.route('/net_montly_table')
def net_montly_table():

    # Query to get month-year, income, and expense, total net saving, for the available month-year
    results = db.session.query(
        func.strftime('%Y-%m', net.date).label('month_year'),
        func.sum(net.amount).label('total'),
        func.sum(case((net.type == 'Income', net.amount), else_=0)).label('total_income'),
        func.sum(case((net.type == 'Expense', func.abs(net.amount)), else_=0)).label('total_expense')
    ).group_by(func.strftime('%Y-%m', net.date)).all()
    
    return render_template('net_montly_table.html', results=results)

@app.route('/net_yearly_table')
def net_yearly_table():

    # Query to get year, income, and expense, total net saving, for the available year
    results = db.session.query(
        func.strftime('%Y', net.date).label('year'),
        func.sum(net.amount).label('total'),
        func.sum(case((net.type == 'Income', net.amount), else_=0)).label('total_income'),
        func.sum(case((net.type == 'Expense', func.abs(net.amount)), else_=0)).label('total_expense')
    ).group_by(func.strftime('%Y', net.date)).all()
    
    return render_template('net_yearly_table.html', results=results)

@app.route('/default_table')
def default_table():

    # Querying both models
    expenses = add_expenses.query.order_by(add_expenses.date.desc()).all()
    incomes = add_incomes.query.order_by(add_incomes.date.desc()).all()

    # Combine the results of query
    entries = combine_table(expenses,incomes)

    return render_template('default_table.html', entries=entries)

@app.route('/default_table_income')
def default_table_income():
    
    # Querying add_incomes models
    incomes = add_incomes.query.order_by(add_incomes.date.desc()).all()

    return render_template('default_table_income.html', incomes=incomes)

@app.route('/default_table_expense')
def default_table_expense():
    # Querying add_expenses models
    expenses = add_expenses.query.order_by(add_expenses.date.desc()).all()

    return render_template('default_table_expense.html', expenses=expenses)

@app.route('/this_month_table')
def this_month_table():
   
    # Get the current month and year, transfer into year-month format
    current_year = datetime.now().year
    current_month = datetime.now().month
    current_year_month = f'{current_year}-{current_month:02d}'

    # Query both models with the condition of year-month 
    expenses = add_expenses.query.filter(func.strftime('%Y-%m', add_expenses.date) == current_year_month).all()
    incomes = add_incomes.query.filter(func.strftime('%Y-%m', add_incomes.date) == current_year_month).all()

    # Combine the the results of query 
    entries = combine_table(expenses,incomes)
    return render_template('default_table.html', entries=entries)

@app.route('/this_month_table_income')
def this_month_table_income():
   
    # Get the current month and year, transfer into year-month format
    current_year = datetime.now().year
    current_month = datetime.now().month
    current_year_month = f'{current_year}-{current_month:02d}'

    # Query add_incomes models with the condition of year-month, sort it by date in descending order
    incomes = add_incomes.query.filter(func.strftime('%Y-%m', add_incomes.date) == current_year_month).all()
    incomes.sort(key=lambda x: x.date, reverse=True)

    return render_template('default_table_income.html', incomes=incomes)

@app.route('/this_month_table_expense')
def this_month_table_expense():
   
    # Get the current month and year, transfer into year-month format
    current_year = datetime.now().year
    current_month = datetime.now().month
    current_year_month = f'{current_year}-{current_month:02d}'
    print(current_year_month)

    # Query add_expenses models with the condition of year-month, sort it by date in descending order
    expenses = add_expenses.query.filter(func.strftime('%Y-%m', add_expenses.date) == current_year_month).all()
    expenses.sort(key=lambda x: x.date, reverse=True)

    return render_template('default_table_expense.html', expenses=expenses)

@app.route('/last_7days_table')
def last_7days_table():

    # Querying both models with the condition of date, only want last 7 days of data
    expenses = add_expenses.query.filter(add_expenses.date > date.today() - timedelta(weeks=1) ).all()
    incomes = add_incomes.query.filter(add_incomes.date > date.today() - timedelta(weeks=1) ).all()

    # Combine the results of query
    entries = combine_table(expenses,incomes)
    return render_template('default_table.html', entries=entries)

@app.route('/last_7days_table_income')
def last_7days_table_income():

    # Querying add_incomes models with the condition of date, only want last 7 days of data, sort it by date in descending order
    incomes = add_incomes.query.filter(add_incomes.date > date.today() - timedelta(weeks=1) ).all()
    incomes.sort(key=lambda x: x.date, reverse=True)

    return render_template('default_table_income.html', incomes=incomes)

@app.route('/last_7days_table_expense')
def last_7days_table_expense():

    # Querying add_expenses models with the condition of date, only want last 7 days of data, sort it by date in descending order
    expenses = add_expenses.query.filter(add_expenses.date > date.today() - timedelta(weeks=1) ).all()
    expenses.sort(key=lambda x: x.date, reverse=True)

    return render_template('default_table_expense.html', expenses=expenses)

@app.route('/addexpense', methods = ["POST", "GET"])
def add_expense():
    form = ExpenseForm()

    # Choices of form is from category model, so we query them, the category only for expense type
    categories = db.session.query(category.category).filter(category.type == 'Expense').all()
    form.category.choices = [(c.category, c.category) for c in categories]

    # When the user clicked the submit button, it saves the data into add_expenses and net models. The net model will save expense and income amount, it will save expense amount in negative form
    if form.validate_on_submit():
        entry = add_expenses(amount=form.amount.data, category=form.category.data, date= form.date.data, nota=form.nota.data)
        nett = net(amount=-abs(form.amount.data), date=form.date.data, type='Expense')
        db.session.add(entry)
        db.session.add(nett)
        db.session.commit()

        flash(f"RM{form.amount.data} has been added ", "success")

        return redirect(url_for('add_expense'))
    
    # Query add_expenses models, sort it by date in descending order
    expenses = add_expenses.query.order_by(add_expenses.date.desc()).all()
    
    return render_template('add_expense.html', title="Add expense", form=form, expenses=expenses )
    
@app.route('/addincome', methods = ["POST", "GET"])
def add_income():
    form = IncomeForm()

    #  Fetch categories to populate dropdown. Choices of form is from category model, so we query them, the category only for income type
    categories = db.session.query(category.category).filter(category.type == 'Income').all()
    form.category.choices = [(c.category, c.category) for c in categories]

    # When the user clicked the submit button, it saves the data into add_incomes and net models. The net model will save expense and income amount, it will save income amount in positive form, which its original format
    if form.validate_on_submit():
        entry = add_incomes(amount=form.amount.data, category=form.category.data, date=form.date.data,  nota=form.nota.data)
        nett = net(amount=(form.amount.data), date=form.date.data, type='Income')
        db.session.add(entry)
        db.session.add(nett)
        db.session.commit()

        flash(f"RM{form.amount.data} has been added", "success")

        return redirect(url_for('add_income'))
    
    # Query add_incomes models, sort it by date in descending order
    incomes = add_incomes.query.order_by(add_incomes.date.desc()).all()
    
    return render_template('add_income.html', title="Add income", form=form, incomes=incomes)

@app.route('/dashboard')
def dashboard():

    def get_month_name(month):
        month_names = ["", "January", "February", "March", "April", "May", "June", 
                    "July", "August", "September", "October", "November", "December"]
        return month_names[int(month)] if month and month.isdigit() else ""

    year = request.args.get('year')
    month = request.args.get('month')
    

    if year and month:
        month_name = get_month_name(month)
        current_month_year = f"{month_name} {year}"
    elif year:
        current_month_year = f"{year}" 
    elif month:
        current_month_year = f"{get_month_name(month)}" 
    else:
        current_month_year = "Overall data"


    condition_expense = (1 == 1)
    condition_income = (1 == 1)

    if year:
        condition_expense = and_(condition_expense, db.extract('year', add_expenses.date) == year)
        condition_income = and_(condition_income, db.extract('year', add_incomes.date) == year)
    
    if month:
        condition_expense = and_(condition_expense, db.extract('month', add_expenses.date) == month)
        condition_income = and_(condition_income, db.extract('month', add_incomes.date) == month)

    
    expenses = db.session.query(db.func.sum(add_expenses.amount)).filter(condition_expense).all()
    expense = [total_expense[0] for total_expense in expenses]

    
    incomes = db.session.query(db.func.sum(add_incomes.amount)).filter(condition_income).all()
    income = [total_income[0] for total_income in incomes]
    
    # Line chart (incomes)
    dates_incomes = db.session.query(db.func.sum(add_incomes.amount), add_incomes.date).filter(condition_income).group_by(add_incomes.date).order_by(add_incomes.date).all()
    over_time_expenditure_income = []
    dates_income_labels = []
    for amount, date in dates_incomes:
        over_time_expenditure_income.append(amount)
        dates_income_labels.append(date.strftime('%d-%m-%Y'))

    # Line chart (expenses)
    dates = db.session.query(db.func.sum(add_expenses.amount), add_expenses.date).filter(condition_expense).group_by(add_expenses.date).order_by(add_expenses.date).all()
    over_time_expenditure = []
    dates_labels = []
    for amount, date in dates:
        over_time_expenditure.append(amount)
        dates_labels.append(date.strftime('%d-%m-%Y'))

    # Bar chart (incomes)
    income_category_amount = db.session.query(add_incomes.category, db.func.sum(add_incomes.amount)).filter(condition_income).group_by(add_incomes.category).all()
    income_category_amounts = []
    income_categorys = []
    for category, amount in income_category_amount:
        income_category_amounts.append(amount)
        income_categorys.append(category)

    # Bar chart (expenses)
    expense_category_amount = db.session.query(add_expenses.category, db.func.sum(add_expenses.amount)).filter(condition_expense).group_by(add_expenses.category).all()
    expense_category_amounts = []
    expense_categorys = []
    for category, amount in expense_category_amount:
        expense_category_amounts.append(amount)
        expense_categorys.append(category)

    return render_template('dashboard.html', 
                           title="Dashboard",
                           current_month_year=current_month_year,
                           sum_expenses=json.dumps(expense),
                           sum_incomes=json.dumps(income),
                           over_time_expenditure=json.dumps(over_time_expenditure),
                           dates_label=json.dumps(dates_labels),
                           over_time_income=json.dumps(over_time_expenditure_income),
                           dates_income=json.dumps(dates_income_labels),
                           income_category_amount=json.dumps(income_category_amounts),
                           income_category=json.dumps(income_categorys),
                           expense_category_amount=json.dumps(expense_category_amounts),
                           expense_category=json.dumps(expense_categorys))

@app.route('/search')
def search():

    # Get the key word in data of inside the search box
    q = request.args.get('q')
    
    if q:
        # Querying both models with the condition of key word
        expenses = db.session.query(add_expenses).filter(add_expenses.nota.icontains(q) | add_expenses.amount.icontains(q) | add_expenses.date.icontains(q)| add_expenses.category.icontains(q)| add_expenses.type.icontains(q)).order_by(add_expenses.date.asc()).all()
        incomes = db.session.query(add_incomes).filter(add_incomes.nota.icontains(q) | add_incomes.amount.icontains(q) | add_incomes.date.icontains(q)| add_incomes.category.icontains(q)| add_incomes.type.icontains(q)).order_by(add_incomes.date.asc()).all()

        # Combine the results of query
        results = combine_table(expenses,incomes)

    else:
        results = []

    return render_template('search_result.html', results=results)

@app.route('/search_income')
def search_income():

    # Get the key word in data of inside the search box
    q = request.args.get('q')
    
    if q:
        # Querying add_incomes models with the condition of key word
        results = db.session.query(add_incomes).filter(add_incomes.nota.icontains(q) | add_incomes.amount.icontains(q) | add_incomes.date.icontains(q)| add_incomes.category.icontains(q)| add_incomes.type.icontains(q)).order_by(add_incomes.date.asc()).all()
    else:
        results = []

    return render_template('search_income.html', results=results)

@app.route('/search_expense')
def search_expense():

    # Get the key word in data of inside the search box
    q = request.args.get('q')
    
    if q:
        # Querying add_expenses models with the condition of key word
        results = db.session.query(add_expenses).filter(add_expenses.nota.icontains(q) | add_expenses.amount.icontains(q) | add_expenses.date.icontains(q)| add_expenses.category.icontains(q)| add_expenses.type.icontains(q)).order_by(add_expenses.date.asc()).all()

    else:
        results = []

    return render_template('search_result.html', results=results)
    
@app.route('/category', methods = ["POST", "GET"])
def categoryy():
    form = create_categoryForm()

    # When the user clicked the submit button, it saves the data into category models. 
    if form.validate_on_submit():
        entry = category(category=form.category.data, type=form.type.data)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('categoryy'))
    
    # Querying category models with the condition of type and sepearte them into two variable
    income = db.session.query(category.category, category.type).filter(category.type == 'Income').all()
    expense = db.session.query(category.category, category.type).filter(category.type == 'Expense').all()
    
    return render_template('category.html', title="Create Category", form=form, income=income, expense=expense)

@app.route('/delete/<string:entry_category>/<string:entry_type>', methods=['POST', 'GET'])
def delete_category(entry_category,entry_type):
    
    # Querying category models with the condition of category and type, and delete it
    entry = category.query.filter_by(category= entry_category, type=entry_type).first()
    db.session.delete(entry)
    db.session.commit()

    flash('Deletion was successful', 'success')
    
    return redirect(url_for('categoryy'))

@app.route('/edit_category/<string:entry_category>/<string:entry_type>', methods=['POST', 'GET'])
def edit_category(entry_category,entry_type):
    form = create_categoryForm()

    # Query based on type (Expense or Income) and category
    sql_query = text('SELECT * FROM category WHERE type = :entry_type AND category = :entry_category')
    result = db.session.execute(sql_query, {'entry_type': entry_type, 'entry_category': entry_category}).fetchone()

    # Pre-fill form fields with the festched result
    if request.method == 'GET':
        form.type.data = result[1]  
        form.category.data = result[2]  

    # If the user clicked save button
    if form.validate_on_submit():
        print('save')
        entry = category.query.filter_by(category= entry_category, type=entry_type).first()
        entry.category=form.category.data
        entry.type=form.type.data
        db.session.commit()
        return redirect(url_for('categoryy'))
    
    return render_template('edit_category.html', form=form)

@app.route('/get_record/<int:entry_id>/<string:entry_type>/<float:entry_amount>/<string:entry_date>', methods=['POST', 'GET'])
def get_record(entry_id, entry_type, entry_amount, entry_date):

    entry_date = datetime.strptime(entry_date, '%Y-%m-%d %H:%M:%S')
    form = IncomeForm() 

    #To comfirm which model I query based on type (Expense or Income), from its models get the data by its id
    table_name = 'add_expenses' if entry_type == 'Expense' else 'add_incomes'
    sql_query = text(f'SELECT * FROM {table_name} WHERE id = :entry_id')
    result = db.session.execute(sql_query, {'entry_id': entry_id}).fetchone()

    # Fetch categories to populate dropdown. Choices of form is from category model, so we query them, the category only for its type
    categories = db.session.query(category.category).filter(category.type == entry_type).all()
    form.category.choices = [(c.category, c.category) for c in categories]

    # Pre-fill form fields with the fetched result
    if request.method == 'GET':
        form.amount.data = result[1]  
        form.category.data = result[2]
        form.date.data = datetime.strptime(result[3], '%Y-%m-%d %H:%M:%S.%f').date()  
        form.nota.data = result[5] if len(result) > 1 else ''
       
        
    # If the user clicked save button
    if form.validate_on_submit():

        if entry_type == 'Expense':
            entry = add_expenses.query.get(entry_id)
            entry.amount=form.amount.data
            entry.category=form.category.data
            entry.date= form.date.data
            entry.nota=form.nota.data

            ent = net.query.filter_by(amount= -abs(entry_amount), date=entry_date, type='Expense').first()
            ent.amount=-abs(form.amount.data)
            ent.date=form.date.data
           
        else: 
            entry = add_incomes.query.get(entry_id)
            entry.amount=form.amount.data
            entry.category=form.category.data
            entry.date= form.date.data
            entry.nota=form.nota.data

            ent = net.query.filter_by(amount= entry_amount, date=entry_date, type='Income').first()
            ent.amount=form.amount.data
            ent.date=form.date.data
     
        db.session.commit()

        next_page = request.args.get('next', '/')
    
        return redirect(next_page)
    

    return render_template('edit.html', form=form)

@app.route('/delete/<int:entry_id>/<string:entry_type>/<float:entry_amount>/<string:entry_date>', methods=['POST', 'GET'])
def delete(entry_id, entry_type, entry_amount, entry_date):
    # Parse the date string into a datetime object
    entry_date = datetime.strptime(entry_date, '%Y-%m-%d %H:%M:%S')
    

    # Identify if it's an expense or income entry and retrieve the correct entry
    if entry_type == 'Expense':
        entry = add_expenses.query.get_or_404(entry_id)
        
    else:
        entry = add_incomes.query.get_or_404(entry_id)
        
    if entry_type == 'Expense':
        ent = net.query.filter_by(amount= -abs(entry_amount), date=entry_date, type=entry_type).first()


    else:
        ent = net.query.filter_by(amount= entry_amount, date=entry_date, type=entry_type).first()

    # Delete both entries
    db.session.delete(entry)
    db.session.delete(ent)
    db.session.commit()

    flash('Deletion was successful', 'success')

    # Determine the page to return to, with a fallback to 'index'
    next_page = request.args.get('next', '/')
    
    # Redirect to the specified page
    return redirect(next_page)

@app.route('/tree', methods=['POST', 'GET'])
def tree():
    form= GoalForm()

    # Get the current month and year, transfer into year-month format
    year = datetime.now().year
    month = datetime.now().month
    current_year_month = f'{year}-{int(month):02d}'

    # Query this goal model with condition of current month and year
    current_goal = goal.query.filter_by(month=month, year=year).first()
    print(current_goal)

    if current_goal:
        goal_amount = current_goal.amount 

    else:
        goal_amount = 0

    print(f'goal_amount{goal_amount}')

    # Query this month total saving
    sql_query = text("""SELECT SUM(amount) FROM net WHERE strftime('%Y-%m', date) = :current_year_month """)
    result = db.session.execute(sql_query, {'current_year_month': current_year_month}).fetchone()

    if result[0]== None:
        current_saving = 0
        
    else:
        current_saving = result[0]
        

    print(f'current_saving{current_saving}')

    if goal_amount == 0 :
        image = "tree_images/tree1.png" 
        progress = 0

    else:  # Avoid division by zero
        progress = (current_saving / goal_amount) * 100
        print(f'Progress: {progress}%')

        if progress <= 25:
            image = "tree_images/tree1.png"
        
        elif progress <= 60:
            image = "tree_images/tree2.png"

        elif progress <=99:
            image = "tree_images/tree3.png"
   
        else:
            progress = 100
            image = "tree_images/tree_goal.jpg" 
        

    if form.validate_on_submit():

        # Check wheather has repeated month and year
        month = int(form.month.data)
        year = form.year.data
        repeat_goal = db.session.query(goal).filter_by(month=month, year=year).first()

        if repeat_goal:
            repeat_goal.amount=form.amount.data
            repeat_goal.month=form.month.data
            repeat_goal.year=form.year.data
            db.session.commit()

        else:
          # Save data into goal model
            entry = goal(amount=form.amount.data, month=form.month.data, year=form.year.data)
            db.session.add(entry)
            db.session.commit()


        return redirect(url_for('tree'))
    
    return render_template('tree.html', title="tree", form=form, goal= goal_amount, image= image, net_monthly_table= current_saving, progres=progress)

@app.route('/compare', methods=['GET', 'POST'])
def compare():

    goall = goal.query.all()

    # Query to sum the amount in the 'net' model, grouped by year-month
    net_query = db.session.query(
        func.sum(net.amount).label('total'),
        func.strftime('%Y-%m', net.date).label('month_year')
    ).group_by(func.strftime('%Y-%m', net.date)).all()

    # Create a dictionary for net results with 'month_year' as key
    net_dict = {result.month_year: result.total for result in net_query}

    amounts = []

    # Loop through each goal entry and compare with the net data
    for goal_entry in goall:
        # Create the formatted 'year-month' string for the goal entry
        month_year = f'{goal_entry.year}-{int(goal_entry.month):02d}'

        # Get the net amount if the month_year exists in net_dict, otherwise set net to 0
        net_amount = net_dict.get(month_year, 0)

        if goal_entry.amount == 0 :
            progress = 0

        else:  # Avoid division by zero
            progress = ( net_amount / goal_entry.amount) * 100
            progress = min(progress, 100)  # Cap progress at 100%

        # Append the results
        amounts.append({
            'id':goal_entry.id,
            'month_year': month_year,
            'goal': goal_entry.amount,
            'net': net_amount,
            'progress' :progress
        })

        amounts.sort(key=lambda x: x['month_year'], reverse=True)

    return render_template('compare_goal.html', amounts=amounts)

@app.route('/delete/<int:entry_id>', methods=['POST', 'GET'])
def delete_goal(entry_id):
    
    # Querying category models with the condition of category and type, and delete it
    entry = goal.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()

    flash('Deletion was successful', 'success')
    
    return redirect(url_for('compare'))

@app.route('/edit_goal/<int:entry_id>', methods=['POST', 'GET'])
def edit_goal(entry_id):
    form = GoalForm()

    sql_query = text(f'SELECT * FROM goal WHERE id = :entry_id')
    result = db.session.execute(sql_query, {'entry_id': entry_id}).fetchone()

    if request.method == 'GET':
        form.amount.data = result[1]  
        form.month.data = result[2]
        form.year.data = result[3]

    if form.validate_on_submit():
        print('save')

        goal_entry = goal.query.get(entry_id)

        goal_entry.amount=form.amount.data
        goal_entry.month=form.month.data
        goal_entry.year=form.year.data
       
        db.session.commit()

        return redirect(url_for('compare'))

    return render_template('edit_goal.html', form=form)

    

@app.route('/tree_goal/<int:entry_id>', methods=['GET'])
def tree_goal(entry_id):

    goal_entry = goal.query.get(entry_id)
    goal_amount = goal_entry.amount
    year = goal_entry.year
    month = goal_entry.month
    current_year_month = f'{year}-{int(month):02d}'

    sql_query = text("""SELECT SUM(amount) FROM net WHERE strftime('%Y-%m', date) = :current_year_month """)
    result = db.session.execute(sql_query, {'current_year_month': current_year_month}).fetchone()

    if result[0]== None:
        current_saving = 0
        
    else:
        current_saving = result[0]

    print(f"goal_amount{goal_amount},current_year_month{current_year_month},net{current_saving}")


    if goal_amount == 0:
        image = "tree_images/tree1.png"
        progress = 0
    else:
        progress = (current_saving / goal_amount) * 100
        if progress <= 25:
            image = "tree_images/tree1.png"
        elif progress <= 60:
            image = "tree_images/tree2.png"
        elif progress <= 99:
            image = "tree_images/tree3.png"
        else:
            image = "tree_images/tree_goal.jpg"
            progress = 100

    return render_template('goal_progress.html', image=image, progress=progress, goal_amount=goal_amount, current_year_month=current_year_month, net=current_saving)

@app.route('/this_year_goaltable')
def this_year_goaltable():
    # Get the current year
    current_year = str(datetime.now().year)  # Ensure it's a string for comparison

    # Query goals for the current year
    goall = goal.query.filter(goal.year == current_year).all()

    # Query to sum the amount in the 'net' model, grouped by year-month
    net_query = db.session.query(
        func.sum(net.amount).label('total'),
        func.strftime('%Y-%m', net.date).label('month_year')  # Adjust for your database
    ).filter(func.strftime('%Y', net.date) == current_year).group_by(func.strftime('%Y-%m', net.date)).all()

    amounts = goal_net(net_query,goall)

    # Combine the results and render template
    return render_template('this_year_goaltable.html', amounts=amounts)

@app.route('/all_goaltable')
def all_goaltable():
    # Get the current year
    goall = goal.query.all()

    # Query to sum the amount in the 'net' model, grouped by year-month
    net_query = db.session.query(
        func.sum(net.amount).label('total'),
        func.strftime('%Y-%m', net.date).label('month_year')
    ).group_by(func.strftime('%Y-%m', net.date)).all()

    amounts = goal_net(net_query,goall)

    return render_template('this_year_goaltable.html', amounts=amounts)

@app.route('/search_year_month',methods=['POST','GET'])
def search_year_month():

    month = request.form.get('month')
    year = request.form.get('year')

    if month == 'all':

        goall = goal.query.filter(goal.year == year).all()

        # Query to sum the amount in the 'net' model, grouped by year-month
        net_query = db.session.query(
            func.sum(net.amount).label('total'),
            func.strftime('%Y-%m', net.date).label('month_year')
        ).filter(func.strftime('%Y', net.date) == year).group_by(func.strftime('%Y-%m', net.date)).all()

    else:

        current_year_month = f'{year}-{int(month):02d}'

        goall = goal.query.filter( goal.month == month, goal.year == year).all()

        # Query to sum the amount in the 'net' model, grouped by year-month
        net_query = db.session.query(
            func.sum(net.amount).label('total'),
            func.strftime('%Y-%m', net.date).label('month_year')
        ).filter(func.strftime('%Y-%m', net.date) == current_year_month).group_by(func.strftime('%Y-%m', net.date)).all()

    amounts = goal_net(net_query,goall)

   
    return render_template('this_year_goaltable.html',amounts=amounts)