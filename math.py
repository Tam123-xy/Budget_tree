# def combine_table(expenses,incomes):
   
#     # Combine the entries
#     entries = []
    
#     # Add expenses to the combined list
#     for expense in expenses:
#         entries.append({
#             'id': expense.id,
#             'date': expense.date,
#             'type': expense.type,
#             'category': expense.category,  # Assuming a category field exists
#             'amount': expense.amount,
#             'nota': expense.nota
#         })
    
#     # Add incomes to the combined list
#     for income in incomes:
#         entries.append({
#             'id': income.id,
#             'date': income.date,
#             'type': income.type,
#             'category': income.category,  # Assuming the source acts as a category
#             'amount': income.amount,
#             'nota': income.nota
#         })

#     # Sort the combined list by date in descending order
#     entries.sort(key=lambda x: x['date'], reverse=True)
#     return entries

# @app.route('/default_table')
# def default_table():
#     # # Querying both models
#     expenses = add_expenses.query.order_by(add_expenses.date.desc()).all()
#     incomes = add_incomes.query.order_by(add_incomes.date.desc()).all()

    
#     entries = combine_table(expenses,incomes)

#     return render_template('default_table.html', entries=entries)

# @app.route('/search')
# def search():
#     q = request.args.get('q')
#     print(q)
    
#     if q:
#         expenses = db.session.query(add_expenses).filter(add_expenses.nota.icontains(q) | add_expenses.amount.icontains(q) | add_expenses.date.icontains(q)| add_expenses.category.icontains(q)| add_expenses.type.icontains(q)).order_by(add_expenses.date.asc()).all()
#         incomes = db.session.query(add_incomes).filter(add_incomes.nota.icontains(q) | add_incomes.amount.icontains(q) | add_incomes.date.icontains(q)| add_incomes.category.icontains(q)| add_incomes.type.icontains(q)).order_by(add_incomes.date.asc()).all()
        
#         results = combine_table(expenses,incomes)

#     else:
#         results = []

#     return render_template('search_result.html', results=results)


# # index,default_table,search

@app.route('/this_month_table')
def this_month_table():

    current_year = datetime.now().year
    current_month = datetime.now().month

    # Format the current year and month to match the strftime pattern (e.g., '2024-09')
    current_year_month = f'{current_year}-{current_month:02d}'
    
    # Debugging statement to check the current year and month
    print(f"Current Year-Month: {current_year_month}")

    # Query expenses for the current month (assuming SQLite or databases supporting strftime)
    expenses = add_expenses.query.filter(
        func.strftime('%Y-%m', add_expenses.date) == current_year_month
    ).all()

     return render_template('this_month_table.html', entries=expenses)


{% for entry in entries %}
<tr>
    <th scope="row">{{loop.index}}</th>
    <td>{{entry.date.strftime("%d-%m-%Y")}}</td>
    <td>{{entry.type}}</td>
    <td>{{entry.category }}</td>
    <td>{{entry.nota }}</td>

    {% if entry.type == 'Expense' %}
    <td class="amount-field">RM <span style="color: rgb(223, 20, 20);">{{ "{:.2f}".format(entry.amount) }}</span></td>
    {% else %}
    <td class="amount-field">RM <span style="color: rgb(49, 81, 207);">{{ "{:.2f}".format(entry.amount) }}</span></td>
    {% endif %}
    <td><a href="{{ url_for('delete', entry_id = entry.id, entry_type=entry.type, entry_amount=entry.amount, entry_date=entry.date.strftime('%Y-%m-%d %H:%M:%S'), next=url_for('index'), type=entry.type ) }}"  class="btn btn-outline-danger btn-sm">Delete</a></td>
</tr>
{% endfor %}