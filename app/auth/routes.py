from flask import Blueprint, render_template, request, session, redirect, url_for
from app.helpers.db import get_user_by_username
import bcrypt

auth_bp = Blueprint('auth', __name__, template_folder="templates")

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user_by_username(username)
        if not user:
            return render_template('auth/login.html', result="Invalid credentials!")

        if user[3] is None:
            valid = user[1] == password
        else:
            valid = bcrypt.checkpw(password.encode("utf-8"), user[3].tobytes())

        if valid:
            session['username'] = username
            session['user_id'] = user[2]
            return redirect(url_for('portfolio.dashboard'))

        return render_template('auth/login.html', result="Invalid credentials!")

    return render_template('auth/login.html', result="")

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
