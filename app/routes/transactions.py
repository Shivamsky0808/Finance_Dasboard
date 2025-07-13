from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required, current_user
from app.models.models import db, Transaction
from app.forms import TransactionForm, FilterForm

transactions_bp = Blueprint('transactions', __name__, url_prefix='/transactions')

@transactions_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        transaction = Transaction(
            amount=form.amount.data,
            transaction_type=form.transaction_type.data,
            category=form.category.data,
            date=form.date.data,
            notes=form.notes.data,
            user_id=current_user.id
        )
        db.session.add(transaction)
        db.session.commit()
        flash('Transaction added successfully!')
        return redirect(url_for('dashboard.index'))
    return render_template('transactions/add_transaction.html', form=form)

@transactions_bp.route('/edit/<int:transaction_id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    if transaction.user_id != current_user.id:
        flash('You are not authorized to edit this transaction.','danger')
        return redirect(url_for('dashboard.index'))
    form = TransactionForm(obj=transaction)
    if form.validate_on_submit():
        transaction.amount = form.amount.data
        transaction.transaction_type = form.transaction_type.data
        transaction.category = form.category.data
        transaction.date = form.date.data
        transaction.notes = form.notes.data
        db.session.commit()
        flash('Transaction updated successfully!')
        return redirect(url_for('dashboard.index'))
    return render_template('transactions/edit_transaction.html', form=form, transaction_id=transaction_id)

@transactions_bp.route('/delete/<int:transaction_id>', methods=['POST'])
@login_required
def delete_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    if transaction.user_id != current_user.id:
        flash('You are not authorized to delete this transaction.','danger')
        return redirect(url_for('dashboard.index'))
    db.session.delete(transaction)
    db.session.commit()
    flash('Transaction deleted successfully!')
    return redirect(url_for('dashboard.index'))

@transactions_bp.route('/list', methods=['GET'])
@login_required
def list_transactions():
    form = FilterForm(request.args)
    query = Transaction.query.filter_by(user_id=current_user.id)
    if form.validate():
        if form.start_date.data:
            query = query.filter(Transaction.date >= form.start_date.data)
        if form.end_date.data:
            query = query.filter(Transaction.date <= form.end_date.data)
        if form.category.data:
            query = query.filter_by(category=form.category.data)
        if form.transaction_type.data:
            query = query.filter_by(transaction_type=form.transaction_type.data)
    
    page = request.args.get('page', 1, type=int)
    transactions = query.paginate(page=page, per_page=current_app.config['TRANSACTIONS_PER_PAGE'])

    return render_template('transactions/list.html', form=form, transactions=transactions)
