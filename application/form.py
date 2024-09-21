from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, DateField, StringField, DecimalField, IntegerField, RadioField
from wtforms.validators import DataRequired, NumberRange, Optional
from datetime import date

class IncomeForm(FlaskForm):
    amount = DecimalField('Amount (RM)', validators = [DataRequired(), NumberRange(min=0.01)]) 
    category = SelectField ('Category', choices=[], validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d',default=date.today,  validators = [DataRequired()])
    nota = StringField('Note (optional)',validators = [Optional()]) 
    submit = SubmitField('Save')

class ExpenseForm(FlaskForm):
    amount = DecimalField('Amount (RM)', validators = [DataRequired(), NumberRange(min=0.01)]) 
    category = SelectField ('Category', choices=[], validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d',default=date.today,  validators = [DataRequired()])
    nota = StringField('Note (optional)', validators = [Optional()]) 
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
    year = IntegerField('Year', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Save Goal')


class create_categoryForm(FlaskForm):
    category = StringField('Category',validators = [DataRequired()]) 
    type =RadioField('Type', choices=[
        ('Income', 'Income'),
        ('Expense', 'Expense')   
        ])
    submit = SubmitField('Create Category')

class CompareForm(FlaskForm):
    month1 = SelectField('Select Month 1', choices=[(i, i) for i in range(1, 13)], coerce=int)
    year1 = IntegerField('Select Year 1', validators=[DataRequired()])
    month2 = SelectField('Select Month 2', choices=[(i, i) for i in range(1, 13)], coerce=int)
    year2 = IntegerField('Select Year 2', validators=[DataRequired()])
    submit = SubmitField('Compare')
    
