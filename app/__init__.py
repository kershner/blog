from flask import Flask
import flask_sqlalchemy

app = Flask(__name__)  # Initialize Flask Object
app.config.from_object('config')
app.secret_key = 'development key'
db = flask_sqlalchemy.SQLAlchemy(app)  # Initialize database

from app import routes, models