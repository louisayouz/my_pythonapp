
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify

from datetime import datetime
from app.helpers.db import all_dividents, delete_div, add_div, edit_div, div_for_quote_and_year, add_full_year_div
from app.helpers.utils import validate_int, validate_string, validate_numeric, symbols_as_array
dividends_bp = Blueprint('dividends', __name__, template_folder="templates")


@dividends_bp.route('/quotedividents', methods=['GET'])
@dividends_bp.route('/quotedividents/<string:quote_symbol>', methods=['GET'])
def quotedividents(quote_symbol=None):
    if quote_symbol:
        # Handle specific quote
        data = all_dividents(quote_symbol)
    else:
        # Handle general case
        data = all_dividents()
    #print(data)
    return render_template('dividents.html', data = data, single_quote = (quote_symbol is not None), quote_symbol = quote_symbol)

@dividends_bp.route('/adddiv', methods=['POST'] )
def adddiv():
    print("POST Data:", request.form)

    symbol = validate_string(request.form['symbol'])
    div_price = validate_numeric(request.form['divprice'])
    div_year = validate_int(request.form['divyear'])
    div_month = validate_int(request.form['divmonth'])

    #print(symbol, div_price, div_year, div_month)

    err=''
    if ( div_price > 0) and (div_year >0  and div_month > 0) and (symbol != ''):
        add_div(symbol.upper(), div_price, div_year, div_month)
    else:
        err = "Invalid quotes parameters"

    return redirect(url_for('dividends.quotedividents', quote_symbol=symbol))


@dividends_bp.route('/editquotediv/<string:value>/<int:id>', methods=['GET'])
def editquotediv(id, value):
    try:
        new_value = float(value)
        edit_div(int(id), value)
    except (TypeError, ValueError):
        return 'Invalid parameters'

    return 'successfully'

@dividends_bp.route('/addyeardiv/<string:quote_symbol>/<int:foryear>', methods=['GET'])
def add_full_year_divs(quote_symbol, foryear):
    add_full_year_div(quote_symbol, foryear, True)
    return redirect(url_for('dividends.quotedividents', quote_symbol=quote_symbol))

@dividends_bp.route('/deletediv/<string:quote_symbol>/<int:divid>', methods=['GET'])
def deletediv(quote_symbol, divid):
    delete_div(divid, quote_symbol)
    return redirect(url_for('dividends.quotedividents', quote_symbol=quote_symbol))

@dividends_bp.route('/importquotedividents/<string:quote_symbol>', methods=['GET'])
def importquotedividents(quote_symbol):
    import_quote(quote_symbol, '2025-01-01', '2025-05-01')
    return redirect(url_for('dividends.quotedividents', quote_symbol=quote_symbol))

@dividends_bp.route('/getquotedivs/<string:quote_symbol>/<int:foryear>/<int:frommonth>/<int:tomonth>', methods=['GET'])
def getquotedivs(quote_symbol,foryear, frommonth, tomonth):
    data = div_for_quote_and_year(quote_symbol,foryear, frommonth, tomonth)
    return jsonify(data)
