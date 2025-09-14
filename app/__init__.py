from flask import Flask, session, redirect, url_for, request
from datetime import timedelta
import os
from app.helpers.db import close_db

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "dev-secret")
    app.permanent_session_lifetime = timedelta(minutes=10)

    # Register blueprints
    from .main.routes import main_bp
    from .auth.routes import auth_bp
    from .portfolio.routes import portfolio_bp
    from .quotes.routes import quotes_bp
    from .dividends.routes import dividends_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(portfolio_bp)
    app.register_blueprint(quotes_bp)
    app.register_blueprint(dividends_bp)


    # Teardown DB
    @app.teardown_appcontext
    def teardown_db(exception):
        close_db()

    # Require login for all except auth/static
    @app.before_request
    def require_login():
        session.permanent = True
        if 'username' not in session and request.endpoint not in ['auth.login', 'static']:
            return redirect(url_for('auth.login'))
    return app

