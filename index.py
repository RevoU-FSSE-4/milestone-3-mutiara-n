from flask import Flask
from dotenv import load_dotenv
from connectors.mysql_connector import connection

from sqlalchemy.orm import sessionmaker

from controllers.users import user_routes
from controllers.accounts import account_routes
from controllers.transactions import transaction_routes
import os

from flask_login import LoginManager
from models.users import Users

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.register_blueprint(user_routes)
app.register_blueprint(account_routes)
app.register_blueprint(transaction_routes)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    Session = sessionmaker(connection)
    s = Session()
    return s.query(Users).get(int(user_id))

@app.route("/")
def hello_world():
    return "Hello World"