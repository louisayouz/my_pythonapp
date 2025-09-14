from flask import Blueprint, render_template, request, session, redirect, url_for
from app.helpers.db import get_user_by_username, save_new_user
import os
import bcrypt

auth_bp = Blueprint('auth', __name__, template_folder="templates")

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    db_psql = False
    if os.environ.get("DB_SUPPORT") == 'postgresql':
        db_psql = True

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user_by_username(username)
        if not user:
            return render_template('auth/login.html', result="Invalid credentials!")

        if user[3] is None:
            valid = user[1] == password
        else:
            hashed = user[3]
            #if db_psql:
            #    hashed = user[3].tobytes()

            valid = bcrypt.checkpw(password.encode("utf-8"), hashed)

        if valid:
            session['username'] = username
            session['user_id'] = user[2]
            return redirect(url_for('portfolio.dashboard'))

        return render_template('auth/login.html', result="Invalid credentials!")

    return render_template('auth/login.html', result="")


@auth_bp.route('/save_new_user/<string:name>/<string:ps>', methods=['GET'])
def create_new_user(name, ps):
    msg = f"New user created!"
    if session['username'] == 'admin':
        save_new_user(name, ps)
    else:
        msg = f"You have not authorities to create new user!"

    return render_template('dashboard.html', username=session['username'], msg=msg)


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
