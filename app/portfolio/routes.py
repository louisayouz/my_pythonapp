from flask import Blueprint, render_template, request, redirect, url_for, session
from datetime import datetime
from app.helpers.db import create_portfolio, delete_portfolio, portfolio_data
from app.helpers.db import copy_portfolio_to_new_year

portfolio_bp = Blueprint('portfolio', __name__, template_folder="templates")

@portfolio_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', username=session['username'])

@portfolio_bp.route('/portfolio', methods=['GET', 'POST'])
def portfolio():
    if request.method == 'POST':
        portfolio_name = request.form.get('portfolio_name')
        if portfolio_name:
            create_portfolio(session['user_id'], portfolio_name)

    data = portfolio_data(session['user_id'])
    return render_template('portfolio/portfolio.html',
                           portfolio=data,
                           user_name=session['username'],
                           for_year=datetime.now().year)

@portfolio_bp.route('/delete_portfolio/<int:portfolioid>')
def delete_user_portfolio(portfolioid):
    delete_portfolio(session['user_id'], portfolioid)
    return redirect(url_for('portfolio.portfolio'))

@portfolio_bp.route('/copy_portfolio/<int:portfolioid>',methods=['POST'])
def copy_portfolio(portfolioid):
    copy_portfolio_to_new_year(portfolioid)
    return 'successfully' #redirect(url_for('portfolio.portfolio'))



