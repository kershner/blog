#!/usr/bin/env python

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, render_template

app = Flask(__name__)  # Creating Flask Object
app.config.from_object('config')

db = SQLAlchemy(app)

app.secret_key = '65413684f65a446g568465d4fv3xc2vsadf5fsadfvxzcvsdf65465421346543654213sd23f1sad3f21sad3f21sad12vb3vx'