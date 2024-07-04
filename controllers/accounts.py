from flask import Blueprint, request, session

from connectors.mysql_connector import connection

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from models.accounts import Accounts
from models.users import Users

from flask_login import login_required, current_user

from decorators.role_checker import id_required

account_routes = Blueprint("account_routes", __name__)

@account_routes.route('/accounts', methods=['GET'])
@login_required
def show_users():
    Session = sessionmaker(connection)
    s = Session()

    try:
        account_query = select(Accounts)
        result = s.execute(account_query)
        accounts = []

        for row in result.scalars():
            accounts.append({
                'user_id': row.user_id,
                'account_type': row.account_type,
                'account_number': row.account_number,
                'balance': row.balance
            })

        return {
            'accounts': accounts,
        }

    except Exception as e:
        return { 'message': 'Unexpected Error' }, 500    
    
@account_routes.route('/accounts/<id>', methods=['GET'])
def get_account(id):
    Session = sessionmaker(connection)
    s = Session()
    s.begin()
    try:
        account = s.query(Accounts).filter(Accounts.id == id).first()

        if account:
            account_data = {
                'user_id': account.user_id,
                'account_type': account.account_type,
                'account_number': account.account_number,
                'balance': account.balance
            }

            return {
                'accounts': account_data
            }
    
    except Exception as e:
        print(e)
        return { 'message': 'Unexpected Error' }, 500    

@account_routes.route('/accounts', methods=['POST'])
def create_account():
    Session = sessionmaker(connection)
    s = Session()

    s.begin()
    try:
        NewAccount = Accounts(
            user_id=request.form['user_id'],
            account_type=request.form['account_type'],
            account_number=request.form['account_number'],
            balance=request.form['balance']
        )
        
        s.add(NewAccount)
        s.commit()
        
    except Exception as e:
        print(e)
        s.rollback()
        return { "message": "Create account failed"}, 500 
       
    return { "message": "New account added" }, 200

@account_routes.route('/accounts/<id>', methods=['PUT'])
def update_account(id):
    Session = sessionmaker(connection)
    s = Session()
    s.begin()

    try:
        account = s.query(Accounts).filter(Accounts.id == id).first()

        account.user_id = request.form['user_id']        
        account.account_type = request.form['account_type']
        account.account_number = request.form['account_number']
        account.balance = request.form['balance']

        s.commit()
        return { 'message': 'Update product success'}, 200
    
    except Exception as e:
        print(e)
        s.rollback()
        return { "message": "Updated Failed" }, 500

@account_routes.route('/accounts/<id>', methods=['DELETE'])
def delete_account(id):
    Session = sessionmaker(connection)
    s = Session()
    s.begin()
    try:
        account = s.query(Accounts).filter(Accounts.id == id).first()
        s.delete(account)
        s.commit()
        return { 'message': 'Success delete product data'}, 200        
    
    except Exception as e:
        print(e)
        s.rollback()
        return { "message": "Fail to Delete" }, 500

    
