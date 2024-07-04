from flask import Blueprint, request

from connectors.mysql_connector import connection

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from models.transactions import Transactions

from flask_login import login_required, current_user

transaction_routes = Blueprint("transaction_route", __name__)

@transaction_routes.route('/transactions', methods=['GET'])
def get_transactions():
    Session = sessionmaker(connection)
    s = Session()

    try:
        transaction_query = select(Transactions)
        result = s.execute(transaction_query)
        transactions = []

        for row in result.scalars():
            transactions.append({
                'from_account_id': row.from_account_id,
                'to_account_id': row.to_account_id,
                'amount': row.amount,
                'type': row.type,
                'description': row.description
            })

        return {
            'transactions': transactions,
        }

    except Exception as e:
        return { 'message' : "Unexpected Error" }, 500

@transaction_routes.route('/transactions/<id>', methods=['GET'])
def transaction_details(id):
    Session = sessionmaker(connection)
    s = Session()
    s.begin()
    try:
        transaction = select(Transactions).filter(Transactions.id == id).first()

        if transaction:
            transaction_data = {
                'from_account_id': Transactions.from_account_id,
                'to_account_id': Transactions.to_account_id,
                'amount': Transactions.amount,
                'type': Transactions.type,
                'description': Transactions.description
        }

        return {
            'transactions': transaction_data
        }
    
    except Exception as e:
        return { 'message': 'Unexpected Error' }, 500    

@transaction_routes.route('/transactions', methods=['POST'])
def new_transaction():
    Session = sessionmaker(connection)
    s = Session()

    s.begin()
    try:
        NewTransaction = Transactions(
            from_account_id=request.form['from_account_id'],
            to_account_id=request.form['to_account_id'],
            amount=request.form['amount'],
            type=request.form['type'],
            description=request.form['description'] 
        )
        
        s.add(NewTransaction)
        s.commit()
        
    except Exception as e:
        print(e)
        s.rollback()
        return { "message": "Create transaction failed"}, 500 
       
    return { "message": "New transaction added" }, 200    