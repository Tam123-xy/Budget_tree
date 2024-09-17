from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, DateField, StringField, DecimalField, IntegerField, RadioField
from wtforms.validators import DataRequired, NumberRange, Optional
from datetime import date

class IncomeForm(FlaskForm):
    amount = DecimalField('Amount (RM)', validators = [DataRequired(), NumberRange(min=0.01)]) 
    # category = SelectField ('Category', validators=[DataRequired()],
    #                                         choices =[('💰Salary', '💰Salary'),
    #                                                   ('💵Bonus','💵Bonus'),
    #                                                   ('💸Allowance','💸Allowance'),
    #                                                   ('🤑Sideline','🤑Sideline')])
    category = SelectField ('Category', choices=[], validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d',default=date.today,  validators = [DataRequired()])
    nota = StringField('Nota (optional)',validators = [Optional()]) 
    submit = SubmitField('Save')

class ExpenseForm(FlaskForm):
    amount = DecimalField('Amount (RM)', validators = [DataRequired(), NumberRange(min=0.01)]) 
    category = SelectField ('Category' , validators=[DataRequired()],
                                            choices  =[('🏡Rent', '🏡Rent'),
                                                      ('🍴 Food and Beverage','🍴 Food and Beverage'),
                                                      ('🛍️ Shopping','🛍️ Shopping'),
                                                      ('🚊 Transport',' 🚊Transport')])
    date = DateField('Date', format='%Y-%m-%d',default=date.today,  validators = [DataRequired()])
    nota = StringField('Nota (optional)', validators = [Optional()]) 
    submit = SubmitField('Save')


class this_month_table_Form(FlaskForm):
    year = IntegerField('Year', validators=[DataRequired(), NumberRange(min=1)])
    month = SelectField ('Month' , validators=[DataRequired()],
                                            choices  =[('1', 'January'),
                                                      ('2','February'),
                                                      ('3','March'),
                                                      ('4',' April'),
                                                      ('5','May'),
                                                      ('6','June'),
                                                      ('7','July'),
                                                      ('8','August'),
                                                      ('9','September'),
                                                      ('10','October'),
                                                      ('11','November'),
                                                      ('12','December')       
                                                      ])
    submit = SubmitField('Done')

class GoalForm(FlaskForm):
    amount = DecimalField('Enter your goal', validators=[DataRequired(),  NumberRange(min=0.01)])
    month = SelectField ('Month' , validators=[DataRequired()],
                                            choices  =[('1', 'January'),
                                                      ('2','February'),
                                                      ('3','March'),
                                                      ('4',' April'),
                                                      ('5','May'),
                                                      ('6','June'),
                                                      ('7','July'),
                                                      ('8','August'),
                                                      ('9','September'),
                                                      ('10','October'),
                                                      ('11','November'),
                                                      ('12','December')       
                                                      ])
    year = IntegerField('Year', validators=[DataRequired(), NumberRange(min=2024, max=2050)])
    submit = SubmitField('Save Goal')


class create_categoryFrom(FlaskForm):
    category = StringField('Category',validators = [DataRequired()]) 
    type =RadioField('Type', choices=[
        ('Income', 'Income'),
        ('Expense', 'Expense')   
        ])
    submit = SubmitField('Create Category')


    
