from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, DateField, StringField, DecimalField
from wtforms.validators import DataRequired, NumberRange, Optional
from datetime import date

class ExpenseForm(FlaskForm):
    amount = DecimalField('Amount (RM)', validators = [DataRequired(), NumberRange(min=0.01)]) 
    category = SelectField ('Category' , validators=[DataRequired()],
                                            choices  =[('🏡Rent', '🏡Rent'),
                                                      ('🍴 Food and Beverage','🍴 Food and Beverage'),
                                                      ('🛍️ Shopping','🛍️ Shopping'),
                                                      ('🚊 Transport',' 🚊Transport')])
    date = DateField('Date', format='%Y-%m-%d', default=date.today, validators = [DataRequired()])
    nota = StringField('Nota (optional)', validators = [Optional()]) 
    submit = SubmitField('Save')

class IncomeForm(FlaskForm):
    amount = DecimalField('Amount (RM)', validators = [DataRequired(), NumberRange(min=0.01)]) 
    category = SelectField ('Category', validators=[DataRequired()],
                                            choices =[('💰Salary', '💰Salary'),
                                                      ('💵Bonus','💵Bonus'),
                                                      ('💸Allowance','💸Allowance'),
                                                      ('🤑Sideline','🤑Sideline')])
    date = DateField('Date', format='%Y-%m-%d',default=date.today,  validators = [DataRequired()])
    nota = StringField('Nota (optional)',validators = [Optional()]) 
    submit = SubmitField('Save')