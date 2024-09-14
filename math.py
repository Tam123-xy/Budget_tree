<form hx-post="/set" hx-target="#results" hx-swap="innerHTML">
    <label for="month">Month</label>
    <select name="month" id="month">
        <option value="1">January</option>
        <option value="2">February</option>
        <option value="3">March</option>
        <option value="4">April</option>
        <option value="5">May</option>
        <option value="6">June</option>
        <option value="7">July</option>
        <option value="8">August</option>
        <option value="9">September</option>
        <option value="10">October</option>
        <option value="11">November</option>
        <option value="12">December</option>
    </select>
    <label for="year">Year</label>
    <input type="number" id="year" name="year" min="1" style="width: 100px;">
    <button type="submit">Set</button>
</form>
<button type="submit"  hx-get="/net" hx-target="#results">Generate table</button>

@app.route('/set', methods=['POST','GET'])
def set():
    month = request.form.get('month')
    year = request.form.get('year')
    print(month)
    print(year)
    current_year_month = f'{year}-{month}'

    expenses = add_expenses.query.filter(func.strftime('%Y-%m', add_expenses.date) == current_year_month).all()
    incomes = add_incomes.query.filter(func.strftime('%Y-%m', add_incomes.date) == current_year_month).all()

    entries = combine_table(expenses,incomes)

    return render_template('default_table.html',entries=entries)
                        