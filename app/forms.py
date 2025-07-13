from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SelectField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange
from datetime import date
from app.models.models import INCOME_CATEGORIES, EXPENSE_CATEGORIES

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class TransactionForm(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0.01)])
    transaction_type = SelectField('Type', choices=[('income', 'Income'), ('expense', 'Expense')], validators=[DataRequired()])
    category = SelectField('Category', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()], default=date.today)
    notes = TextAreaField('Notes', validators=[Length(max=200)])
    submit = SubmitField('Save Transaction')
    
    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        # Set category choices based on transaction type
        self.category.choices = [(cat, cat) for cat in INCOME_CATEGORIES + EXPENSE_CATEGORIES]

class FilterForm(FlaskForm):
    start_date = DateField('Start Date')
    end_date = DateField('End Date')
    category = SelectField('Category', choices=[('', 'All Categories')])
    transaction_type = SelectField('Type', choices=[('', 'All Types'), ('income', 'Income'), ('expense', 'Expense')])
    submit = SubmitField('Apply Filters')
    
    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        all_categories = [('', 'All Categories')]
        all_categories.extend([(cat, cat) for cat in INCOME_CATEGORIES + EXPENSE_CATEGORIES])
        self.category.choices = all_categories
