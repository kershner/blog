from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
                           title="Home")

@app.route('/about')
def about():
    return render_template("about.html",
                           title="About Me")


@app.route('/projects')
def projects():
    return render_template("projects.html",
                           title="Projects")