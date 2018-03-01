from flask import jsonify, render_template, request
from modules import old_routes
from app import app


##############################################################################
# Blog #######################################################################
@app.route('/')
def portfolio():
    return render_template('/portfolio/portfolio.html')

if __name__ == '__main__':
    app.run()
