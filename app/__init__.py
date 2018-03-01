from flask import Flask
import flask_sqlalchemy

app = Flask(__name__)  # Initialize Flask Object
app.config.from_object('config')
db = flask_sqlalchemy.SQLAlchemy(app)  # Initialize database

# from app import routes
