from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from app.helpers.db import get_user_by_username, save_new_user
from app.helpers.db import payments, new_payment, remove_payment, change_payment, get_payment
from app.constants import CURRENT_YEAR
from datetime import datetime
import os
import bcrypt
from decimal import Decimal

vaad_bp = Blueprint('vaad', __name__, template_folder="templates")
@vaad_bp.route('/vaad', methods=['GET', 'POST'])
def vaad():
  result = {}
  result = payments()
  #print(result)
  return render_template('vaad/vaad.html', data=result, cur_year = CURRENT_YEAR, appname='vaad')

@vaad_bp.route('/vaad_add_payment', methods=['POST'] )
def vaad_add_payment():
   app_id = int(request.form['app_id'])
   payment = Decimal(request.form['payment'])
   for_year = int(request.form['for_year'])
   new_payment(for_year, app_id, payment)
   return redirect(url_for('vaad.vaad'))

@vaad_bp.route('/remove_payment/<int:payment_id>', methods=['GET'] )
def vaad_remove_payment(payment_id):
   remove_payment(payment_id)
   return redirect(url_for('vaad.vaad'))

@vaad_bp.route('/edit_payment', methods=['POST'])
def vaad_edit_payment():
   payment_id = int(request.form['payment_id'])
   app_id = int(request.form['app_id'])
   payment = Decimal(request.form['payment'])
   pay_year = CURRENT_YEAR
   payed_at = request.form['payed_at']

   dt_object = datetime.strptime(payed_at, "%d-%m-%Y")
   now = datetime.now()

   dt_object = dt_object.replace(
      hour=now.hour,
      minute=now.minute,
      second=now.second
   )

   change_payment(payment_id, app_id, payment, pay_year, dt_object)
   return redirect(url_for('vaad.vaad'))

@vaad_bp.route('/receipt/<int:payment_id>', methods=['GET'])
def receipt(payment_id):

  result = {}
  result = get_payment(payment_id)
  print(result)
  return render_template('vaad/receipt.html', data=result, cur_year = CURRENT_YEAR, appname='vaad')
