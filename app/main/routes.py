from flask import Blueprint, redirect, url_for, session

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    if "username" in session:
        return redirect(url_for("portfolio.dashboard"))

    return redirect(url_for("auth.login"))

