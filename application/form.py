from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired

class ExpenseForm(FlaskForm):
    amount = IntegerField('Amount', validators = [DataRequired()]) 
    category = SelectField ('Category', validators=[DataRequired()],
                                            choices =[('Rent', 'Rent'),
                                                      ('Food and Beverage','Food and Beverage'),
                                                      ('Shopping','Shopping'),
                                                      ('Transport','Transport')])
    date = DateField('Date', format='%Y-%m-%d', validators = [DataRequired()])
    submit = SubmitField('Save')