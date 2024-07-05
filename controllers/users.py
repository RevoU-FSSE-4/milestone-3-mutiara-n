from flask import Blueprint, request
from connectors.mysql_connector import connection
from models.users import Users

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from flask_login import login_user, login_required, logout_user, current_user

user_routes = Blueprint("user_routes", __name__)

@user_routes.route('/users', methods=['POST'])
def register_user():
    Session = sessionmaker(connection)
    s = Session()
    s.begin()

    try:
        NewUser = Users(
            username=request.form['username'],
            email=request.form['email']
        )
        
        NewUser.set_password(request.form['password_hash'])

        s.add(NewUser)
        s.commit()

    except Exception as e:
        print(e)
        s.rollback()
        return { "message": "Register Failed"}, 500
    
    return { "message": "Register Success" }, 200

@user_routes.route('/users/login', methods=['POST'])
def check_login():
    Session = sessionmaker(connection)
    s = Session()
    s.begin()

    try:
        email = request.form['email']
        user = s.query(Users).filter(Users.email == email).first()

        if user == None:
            return { "message": "User not found" }, 403
        
        if not user.check_password(request.form['password']):
            return { "message": "Invalid password" }, 403
        
        login_user(user)

        session_id = request.cookies.get('session')

        return {
            "session_id": session_id,
            "message": "Login Success"
        }, 200

    except Exception as e:
        s.rollback()
        print(e)
        return { "message": "Login Failed" }, 500    
    
@user_routes.route('/users/me', methods=['GET'])
@login_required
def get_user():
    Session = sessionmaker(connection)
    s = Session()

    try:
        user_query = select(Users)
        s.execute(user_query)
        user = {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email
        }

        return {
            'user': user        
        }

    except Exception as e:
        return { 'message': 'Unexpected Error' }, 500
    
@user_routes.route('/users/me', methods=['PUT'])
@login_required
def update_user():
    Session = sessionmaker(connection)
    s = Session()
    s.begin()
    
    try:
        user = s.query(Users).filter(Users.id == current_user.id).first()

        if not user:
            return {"message": "User not found"}, 404

        user.username = request.form['username']
        user.email = request.form['email']
        
        s.commit()
        return {"message": "Update user data success"}, 200

    except Exception as e:
        print(str(e))
        s.rollback()
        return { "message": "Update Failed", 'error': str(e)}, 500

@user_routes.route('/users/logout', methods=['GET'])
@login_required
def user_logout():
    logout_user()
    return { "message": "Logout Success" }