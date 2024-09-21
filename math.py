@app.route('/tree', methods=['POST', 'GET'])
def tree():
    form = GoalForm()

    if form.validate_on_submit():
        goal_amount = form.amount.data if form.amount.data else 0  # Set amount = 0 if user doesn't enter a value
        entry = goal(amount=form.amount.data, month=form.month.data, year=form.year.data)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('tree'))
    
    # Fetch the latest goal from the database
    current_goal = db.session.query(goal).order_by(goal.id.desc()).first()
    
    # Decide which image to display based on current progress
    goal_amount = 100  # Your goal amount, or fetch it from the database
    image = "tree_images/tree1.png"  # Default image

    if current_goal:
        month = current_goal.month
        year = current_goal.year

        current_year_month = f'{year}-{int(month):02d}'

        sum_income = db.session.query(
            db.func.sum(add_incomes.amount)
        ).filter(
            func.strftime('%Y-%m', add_incomes.date) == current_year_month
        ).scalar() or 0  # Ensure it returns 0 if no result

        sum_expense = db.session.query(
            db.func.sum(add_expenses.amount)
        ).filter(
            func.strftime('%Y-%m', add_expenses.date) == current_year_month
        ).scalar() or 0  # Ensure it returns 0 if no result

        current_saving = sum_income - sum_expense

        # Set default image
        image = "tree_images/tree1.png"
        goal_amount = current_goal.amount

        if goal_amount > 0:  # Avoid division by zero
            progress = (current_saving / goal_amount) * 100
            if progress >= 100:
                image = "tree_images/tree_goal.jpg"  # Goal achieved
            elif progress >= 67:
                image = "tree_images/tree3.png"  # More than 66% progress
            elif progress >= 34:
                image = "tree_images/tree2.png"  # Between 34% and 66% progress
            else:
                image = "tree_images/tree1.png"  # Less than 34% progress

    else:
        current_saving = 0
        image = "tree_images/tree1.png"  # Default image if no goal exists

    return render_template('tree.html', title="tree", form=form, goal=current_goal, image=image, net_monthly_table=current_saving)