from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from app.models.models import db, Transaction
from sqlalchemy import func, extract
from datetime import datetime, timedelta
import json

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/')

@dashboard_bp.route('/')
@login_required
def index():
    # Get basic stats
    total_income = db.session.query(func.sum(Transaction.amount)).filter_by(
        user_id=current_user.id, transaction_type='income'
    ).scalar() or 0
    
    total_expenses = db.session.query(func.sum(Transaction.amount)).filter_by(
        user_id=current_user.id, transaction_type='expense'
    ).scalar() or 0
    
    net_savings = total_income - total_expenses
    
    # Get recent transactions
    recent_transactions = Transaction.query.filter_by(user_id=current_user.id)\
        .order_by(Transaction.date.desc()).limit(5).all()
    
    return render_template('dashboard/index.html', 
                         total_income=total_income,
                         total_expenses=total_expenses,
                         net_savings=net_savings,
                         recent_transactions=recent_transactions)

@dashboard_bp.route('/api/category-spending')
@login_required
def category_spending():
    """API endpoint for category-wise spending pie chart"""
    category_data = db.session.query(
        Transaction.category,
        func.sum(Transaction.amount).label('total')
    ).filter_by(
        user_id=current_user.id,
        transaction_type='expense'
    ).group_by(Transaction.category).all()
    
    data = {
        'labels': [item.category for item in category_data],
        'amounts': [float(item.total) for item in category_data]
    }
    
    return jsonify(data)

@dashboard_bp.route('/api/monthly-comparison')
@login_required
def monthly_comparison():
    """API endpoint for monthly income vs expenses bar chart"""
    # Get data for the last 6 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    
    monthly_data = db.session.query(
        extract('year', Transaction.date).label('year'),
        extract('month', Transaction.date).label('month'),
        Transaction.transaction_type,
        func.sum(Transaction.amount).label('total')
    ).filter(
        Transaction.user_id == current_user.id,
        Transaction.date >= start_date
    ).group_by(
        extract('year', Transaction.date),
        extract('month', Transaction.date),
        Transaction.transaction_type
    ).all()
    
    # Process data for Chart.js
    months = []
    income_data = []
    expense_data = []
    
    # Create a dictionary to organize data by month
    data_by_month = {}
    for item in monthly_data:
        month_key = f"{int(item.year)}-{int(item.month):02d}"
        if month_key not in data_by_month:
            data_by_month[month_key] = {'income': 0, 'expense': 0}
        data_by_month[month_key][item.transaction_type] = float(item.total)
    
    # Generate list of months for the chart
    current_date = start_date
    while current_date <= end_date:
        month_key = f"{current_date.year}-{current_date.month:02d}"
        month_label = current_date.strftime("%b %Y")
        
        months.append(month_label)
        income_data.append(data_by_month.get(month_key, {}).get('income', 0))
        expense_data.append(data_by_month.get(month_key, {}).get('expense', 0))
        
        # Move to next month
        if current_date.month == 12:
            current_date = current_date.replace(year=current_date.year + 1, month=1)
        else:
            current_date = current_date.replace(month=current_date.month + 1)
    
    data = {
        'labels': months,
        'income': income_data,
        'expenses': expense_data
    }
    
    return jsonify(data)
