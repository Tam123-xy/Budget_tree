# income = [1,2,3]
# expense = [50.1044]

# # Calculate the net and round it to two decimal places
# net = [round(income[0] - expense[0], 2)]

# print(net)

# category =['income', 'expense',' net']
# for i in category:
#     print(i)

# my index page and add_expense page have the delete function, I want return redirect to own page


# @app.route('/delete/<int:entry_id>/<string:entry_type>', methods=['POST', 'GET'])
# def delete(entry_id, entry_type):
#     if entry_type == 'Expense':
#         entry = add_expenses.query.get_or_404(entry_id) 
        
#     else:
#         entry = add_incomes.query.get_or_404(entry_id) 
    
#     db.session.delete(entry)
#     db.session.commit()
#     flash('Deletion was success', 'success')
#     return redirect(url_for('index'))

# sum_expense = []

# # Check if the list is empty, not if it's None
# if not sum_expense:
#     (sum_expense[0]) = 0

# print(sum_expense[0])


# sum_expenses = db.session.query(db.func.sum(add_expenses.amount)).all()
# sum_incomes = db.session.query(db.func.sum(add_incomes.amount)).all()
    
#     if sum_expenses is None :
#         sum_expense = [expense[0] for expense in sum_expenses]
#         net  = [sum_expense]

#     elif sum_incomes is None:
#         sum_income = [income[0] for income in sum_incomes]
#         net  = [sum_income]

#     elif sum_expenses is None and sum_incomes is None:
#         net = [0]

#     else:
#         sum_expense = [expense[0] for expense in sum_expenses]
#         sum_income = [income[0] for income in sum_incomes]
#         net = [round(sum_income[0] - sum_expense[0], 2)]

# the computer cannot detect if it is None



    # sum_expenses = db.session.query(db.func.sum(add_expenses.amount)).all()
    # sum_expense = [expense[0] for expense in sum_expenses]

    # sum_incomes = db.session.query(db.func.sum(add_incomes.amount)).all()
    # sum_income = [income[0] for income in sum_incomes]

    # if sum_expense[0] is None and sum_incomes[0] is None:
    #     sum_income[0] = 0
    #     sum_income = [int(i) for i in sum_income]

    #     sum_expense[0] = 0
    #     net = [int(0)]
    
{% for expense in sum_expense %}
            {% for income in sum_income %}
            {% for net_save in net %}
                    <tr>
                        <td class="amount-field">RM <span style="color: rgb(49, 81, 207);">{{ "{:.2f}".format(income) }}</span></td>
                        <td class="amount-field">RM <span style="color: rgb(223, 20, 20);">{{ "{:.2f}".format(expense) }}</span></td>
                        <td class="amount-field">{{  'RM ' + "{:.2f}".format(net_save) }}</td>
                    </tr>
            {% endfor %}
            {% endfor %}
            {% endfor %}

sum_expenses = db.session.query(db.func.sum(add_expenses.amount)).all()
    sum_expense = [expense[0] for expense in sum_expenses]

    sum_incomes = db.session.query(db.func.sum(add_incomes.amount)).all()
    sum_income = [income[0] for income in sum_incomes]
    
    # can
    if sum_expense[0] is None : 
        sum_expense[0] = 0
        net  = [int(i) for i in sum_expense]

    # can
    elif sum_income[0] is None:
        sum_income[0] = 0
        net  = [int(i) for i in sum_income]

    # cannot
    elif sum_expense[0] is None and sum_incomes[0] is None:
        sum_expense[0] = 0
        sum_expense  = [int(i) for i in sum_expense]

        sum_incomes[0] = 0
        sum_incomes  = [int(i) for i in sum_incomes]

        net = [int(0)]

    # can 
    else:
        net = [round(sum_income[0] - sum_expense[0], 2)]

can you fix the cannot, <td class="amount-field">RM <span style="color: rgb(49, 81, 207);">{{ "{:.2f}".format(income) }}</span></td>
TypeError: unsupported format string passed to NoneType.__format__

@app.route('/search')
def search():
    q = request.args.get('q')
    print(q)
    
    if q:
        results = db.session.query(add_expenses).filter(add_expenses.nota.ilike(f'%{q}%') | add_expenses.amount.ilike(f'%{q}%')).order_by(add_expenses.date.asc()).all()

    else:
        results = []

    return render_template('search_result.html', results=results)


{ % for result in results %}
<tr>
    <td>{{result.date.strftime("%d-%m-%Y")}}</td>
    <td>{{result.type}}</td>
    <td>{{result.category }}</td>
    <td>{{result.nota }}</td>
</tr>
{ % endfor %}