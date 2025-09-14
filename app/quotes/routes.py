from flask import Blueprint, render_template, request, redirect, url_for, session
from datetime import datetime
from app.helpers.db import create_portfolio, delete_portfolio, portfolio_data, portfolio_quotes,update_quote_prices
from app.helpers.db import all_symbols, all_dividents, add_quote, refresh_quotes
from app.helpers.db import delete_protfolio_quote, edit_quote, all_dividents, add_div, delete_div, div_for_quote_and_year
from app.helpers.utils import validate_int, validate_string, validate_numeric, symbols_as_array

quotes_bp = Blueprint('quotes', __name__, template_folder="templates")

@quotes_bp.route('/quotes/<int:portfolioid>')
@quotes_bp.route('/quotes/<int:portfolioid>/<int:calcyear>', methods=['GET'])
def quotes(portfolioid, calcyear=None):
    data = portfolio_quotes(portfolioid, calcyear)
    if calcyear is None:
        for_year = datetime.now().year
    else:
        for_year = calcyear

    #print(data)
    err = request.args.get('err') or ''
    return render_template('quotes/quotes.html', quotes=data, symbols = symbols_as_array(data), user_name=session['username'], portfolioid=portfolioid, for_year=for_year, err=err)

@quotes_bp.route('/addquote', methods=['POST'] )
def addquote_to_portfolio():
    print("POST Data:", request.form)
    portfolio_id = validate_int(request.form['portfolioid'])
    symbol = validate_string(request.form['symbol'])
    price = validate_numeric(request.form['price'])
    quotes_count = validate_int(request.form['quantity'])

    from_year = validate_int(request.form['from_year'])
    from_month = validate_int(request.form['from_month'])
    to_year = validate_int(request.form['to_year'])
    if to_year == 0:
        to_year = None
    to_month = validate_int(request.form['to_month'])
    if to_month == 0:
        to_month = None

    err=''
    if (portfolio_id > 0) and ( price > 0) and (quotes_count >0 ) and (symbol != ''):
        add_quote(portfolio_id, symbol.upper(), price, quotes_count, from_year, from_month, to_year, to_month)
    else:
        err = "Invalid quotes parameters"


    return redirect(url_for('quotes.quotes', portfolioid=portfolio_id, calcyear=from_year, err=err))

@quotes_bp.route('/deletequote/<int:portfolioid>/<int:quoteid>', methods=['GET'] )
def delete_quote_to_portfolio(portfolioid, quoteid):
    delete_protfolio_quote(portfolioid, quoteid)

    return redirect(url_for('quotes.quotes', portfolioid=portfolioid))

@quotes_bp.route('/editquote', methods=['POST'] )
def edit_quote_to_portfolio():
    portfolio_id = request.form['portfolioid']
    quote_id = request.form['quoteid']
    price = request.form['price']
    quotes_count = request.form['quantity']

    from_year = validate_int(request.form['from_year'])
    from_month = validate_int(request.form['from_month'])
    to_year = validate_int(request.form['to_year'])
    if to_year == 0:
        to_year = None
    to_month = validate_int(request.form['to_month'])
    if to_month == 0:
        to_month = None


    edit_quote( portfolio_id, quote_id, price, quotes_count, from_year, from_month, to_year, to_month)
    return redirect(url_for('quotes.quotes', portfolioid=portfolio_id, calcyear=from_year))

@quotes_bp.route('/quotedividents', methods=['GET'])
@quotes_bp.route('/quotedividents/<string:quote_symbol>', methods=['GET'])
def quotedividents(quote_symbol=None):
    if quote_symbol:
        # Handle specific quote
        data = all_dividents(quote_symbol)
    else:
        # Handle general case
        data = all_dividents()
    #print(data)
    return render_template('dividends/dividents.html', data = data, single_quote = (quote_symbol is not None), quote_symbol = quote_symbol)

@quotes_bp.route('/symbols', methods=['GET'])
def symbols():
    symbols = all_symbols()
    return render_template('quotes/symbols.html', symbols=symbols)

@quotes_bp.route('/deletesymbol/<string:symbol>', methods=['GET'] )
def deletesymbol(symbol):
    delete_symbol(symbol)
    return render_template('quotes/symbols.html', symbols=all_symbols())
   # return redirect(url_for('quotes', portfolioid=portfolioid))

@quotes_bp.route('/refresh_stocks', methods=['POST'] )
def refresh_stocks():
    refresh_quotes()
    return 'successfully'

@quotes_bp.route('/editquotecloseprice/<string:symbol>/<string:close_price_date>/<string:price>', methods=['POST'] )
def editquotecloseprice(symbol, close_price_date, price ):
    symbol = validate_string(symbol)
    close_date = validate_string(close_price_date)
    price = validate_numeric(price)

    if price == 0 or close_date=='' or symbol=='':
        return 'failed'

    print(f"{symbol} {close_price_date} {price}")
    update_quote_prices([[symbol, price]], close_price_date)
    return 'successfully'

