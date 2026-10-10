from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from app.helpers.db import get_user_by_username, save_new_user
from app.helpers.db import payments, new_payment, remove_payment, change_payment, get_payment
from app.constants import CURRENT_YEAR
from datetime import datetime
import os
import bcrypt
from decimal import Decimal

calculators_bp = Blueprint('calculators', __name__, template_folder="templates")
@calculators_bp.route('/calculators', methods=['GET', 'POST'])
def calculators():
  return render_template('calculators/pension.html', appname='vaad')

