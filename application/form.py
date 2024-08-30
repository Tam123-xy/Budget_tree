from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, IntegerField, DateField, StringField
from wtforms.validators import DataRequired


class ExpenseForm(FlaskForm):
    amount = IntegerField('Amount', validators = [DataRequired()]) 
    category = SelectField ('Category', validators=[DataRequired()],
                                            choices  =[('🏡Rent', '🏡Rent'),
                                                      ('🍴 Food and Beverage','🍴 Food and Beverage'),
                                                      ('🛍️ Shopping','🛍️ Shopping'),
                                                      ('🚊 Transport',' 🚊Transport')])
    date = DateField('Date', format='%Y-%m-%d', validators = [DataRequired()])
    nota = StringField('Nota (optional)', validators = [DataRequired()]) 
    submit = SubmitField('Save')

class IncomeForm(FlaskForm):
    amount = IntegerField('Amount', validators = [DataRequired()]) 
    category = SelectField ('Category', validators=[DataRequired()],
                                            choices =[('💰Salary', '💰Salary'),
                                                      ('💵Bonus','💵Bonus'),
                                                      ('Allowance','Allowance'),
                                                      ('Sideline','Sideline')])
    date = DateField('Date', format='%Y-%m-%d', validators = [DataRequired()])
    nota = StringField('Nota (optional)', validators = [DataRequired()]) 
    submit = SubmitField('Save')