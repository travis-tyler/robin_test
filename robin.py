import click, json, robin_stocks as rh
import ui, funcs, config
from datetime import datetime

@click.group()
def main():
    rh.login(config.user, config.pw)

@main.command(help='Gets the information associated with the accounts profile being held by Robinhood.')
@click.option('--fetch', type=click.STRING)
def info(fetch):
    print(f'\nFetching {fetch}....\n')
    result = rh.load_account_profile()

    if fetch is not None:
        ui.success(result[fetch])
    else:
        ui.success(result)

@main.command(help='Gets a stock quote for one or more symbols')
@click.argument('symbols', nargs=-1)
def quote(symbols):
    quotes = rh.get_quotes(symbols)

    for quote in quotes:
        ui.success(f"\n{quote['symbol']} | {quote['last_extended_hours_trade_price']}\n")

@main.command(help='Gets help for all stocks in your watchlist')
def watchlist():
    print('\nGetting quotes for watchlist....\n')
    
    with open('watchlist') as f:
        symbols = f.read().splitlines()

    quotes = rh.get_quotes(symbols)

    for quote in quotes:
        ui.success(quote)
        ui.bar()

@main.command(help='Buys quantity of stock by symbol')
@click.argument('quantity', type=click.INT)
@click.argument('symbol', type=click.STRING)
@click.option('--limit', type=click.FLOAT)
def buy(quantity, symbol, limit):
    if limit is not None:
        ui.success(f"Bying {quantity} of {symbol} at ${limit}")
        result = rh.order_buy_limit(symbol, quantity, limit)
    else:
        ui.success(f'Bying {quantity} of {symbol} at market price....\n')
        result = rh.order_buy_market(symbol, quantity)

    ui.chec_ref(result)

@main.command(help='Sells quantity of stock by symbol')
@click.argument('quantity', type=click.INT)
@click.argument('symbol', type=click.STRING)
@click.option('--limit', type=click.FLOAT)
def sell(quantity, symbol, limit):
    if limit is not None:
        ui.success(f"\nSelling {quantity} of {symbol} at ${limit}\n")
        result = rh.order_sell_limit(symbol, quantity, limit)
    else:
        ui.success(f'\nSelling {quantity} of {symbol} at market price....\n')
        result = rh.order_sell_market(symbol, quantity)
    ui.chec_ref(result)

@main.command(help='Buys fractional shares by symbol')
@click.argument('amount', type=click.FLOAT)
@click.argument('symbol', type=click.STRING)
def buy_frac(amount, symbol):
    ui.success(f'\nBuying ${amount} of {symbol}....\n')
    result = rh.order_buy_fractional_by_price(symbol, amount)
    ui.chec_ref(result)

@main.command(help='Represents the historicl data for a stock.')
@click.argument('symbol', type=click.STRING)
@click.option('--interval', type=click.STRING)
@click.option('--span', type=click.STRING)
def history(symbol, interval, span):
    ui.success(f'\nGetting {interval} stock historicals for {symbol} for the past {span}....\n')
    result = rh.get_stock_historicals(symbol, interval, span)

    for i in result:
        for x in i:
            ui.success(f'{x}: {i[x]}')
        ui.bar()

@main.command(help='Gets crypto quote by symbol.')
@click.argument('symbol', type=click.STRING)
def crypto_quote(symbol):
    result = rh.get_crypto_quote(symbol)
    ui.success(result)

@main.command(help='Gets historical information about a crypto including open price, close price, high price, and low price.')
@click.argument('symbol', type=click.STRING)
@click.option('--interval', type=click.STRING)
@click.option('--span', type=click.STRING)
def crypto_history(symbol, interval, span):
    ui.success(f'\nGetting {interval} stock historicals for {symbol} for the past {span}....\n')
    result = rh.get_crypto_historicals(symbol, interval, span)

    for i in result:
        for x in i:
            ui.success(f'{x}: {i[x]}')
        ui.bar()

@main.command(help='Places order for crypto with symbol and price.')
@click.argument('symbol', type=click.STRING)
@click.argument('amount', type=click.FLOAT)
def buy_crypto(symbol, amount):
    ui.success(f'Ordering ${amount} of {symbol}....\n')
    result = rh.order_buy_crypto_by_price(symbol, amount)
    ui.chec_ref(result)

@main.command(help='Places order for Dogecoin with symbol and price.')
@click.argument('amount', type=click.FLOAT)
def buy_doge(amount):
    ui.success(f'Ordering ${amount} of DOGE....\n')
    # Doge error workaround
    price = float(rh.get_crypto_quote('DOGE').get('ask_price'))
    shares = round(amount/price, 0)
    result = rh.order_buy_crypto_by_quantity('DOGE', shares)

    ui.chec_ref(result)
    
@main.command(help='Generates support and resistance data from stock history by symbol.')
@click.argument('symbol', type=click.STRING)
@click.option('--interval', type=click.STRING)
@click.option('--span', type=click.STRING)
def get_lines(symbol, interval, span):
    ui.success(f'\nGetting {interval} stock historicals for {symbol} for the past {span}....\n')
    result = rh.get_stock_historicals(symbol, interval, span)

    price = rh.get_quotes(symbol)[0]['last_extended_hours_trade_price']

    ui.bar()
    print(f"Value: {price}")
    ui.bar()
    df = funcs.make_df(result)
    funcs.get_s_r(df)
    ui.bar()

@main.command(help='Returns day trade history.')
def day_trades():
    result = rh.get_day_trades()
    ui.success(len(result))






#OPTIONS
@main.command(help='Submits a limit order for an option. i.e. place a long call or a long put.')
@click.argument('buy_close', type=click.STRING)
#??????????????
@click.argument('credit_debit', type=click.STRING)
@click.argument('price', type=click.FLOAT)
@click.argument('symbol', type=click.STRING)
# @click.argument('quantity', type=click.INT)
@click.argument('date', type=click.STRING)
@click.argument('strike', type=click.FLOAT)
@click.argument('option_type', type=click.STRING)
@click.option('--time_in_force', type=click.STRING)
def buy_option(buy_close, credit_debit, symbol, price, symbol, option_type, date, strike):

    # Covert date
    if len(date.split('/')[0]) == 1:
        month = '0' + date.split('/')[0]
    else:
        month = date.split('/')[0]
    if len(date.split('/')[1]) == 1:
        day = '0' + date.split('/')[0]
    else:
        day = date.split('/')[0]
    today = datetime.today()
    exp_date = f'{month}/{day}/{str(today.year)}'

    # Convert position_effect
    if buy_close == 'BTO':
        position_effect = 'buy'
    elif buy_close == 'BTC':
        position_effect == 'close'
    else:
        print('Invalid position effect')

    # Convert option_type
    if option_type == 'C':
        call_put = 'call'
    elif option_type == 'P':
        call_put == 'put'
    else:
        print('Invalid option type')

    #EXAMPLE = BTO GME 50 P 2/12 4.85
    result = rh.order_buy_option_limit(position_effect, credit_debit(?), price, quantity = 1, strike, exp_date)
    ui.chec_ref(result)







@main.command(help='Gets the information associated with the portfolios profile.')
def portfolio():
    print('Loading portfolio profile....')
    result = rh.load_portfolio_profile()
    ui.success(result)

@main.command(help='Gets the information associated with the portfolios profile.')
def investments():
    print('\nLoading investment profile....\n')
    result = rh.load_investment_profile()
    ui.success(result)
    
@main.command(help='Represents the historical data for a stock.')
@click.argument('symbol', type=click.STRING)
def ratings(symbol):
    ui.success(f'\nGet stock ratings for {symbol}....\n')
    result = rh.get_ratings(symbol)
    ui.success(result)

@main.command(help='Returns the earnings for the different financial quarters.')
@click.argument('symbol', type=click.STRING)
def get_earnings(symbol):
    result = rh.get_earnings(symbol)
    ui.success(result)

@main.command(help='Builds a dictionary of important information regarding the stocks and positions owned by the user.')
def holdings():
    result = rh.build_holdings()
    ui.success(result)

@main.command(help='Returns a list containing every position ever traded.')
def all_positions():
    print('\nRetrieving all positions ever traded....\n')
    result = rh.get_all_positions()
    ui.success(result)

@main.command(help='Returns a list of stocks that are currently held.')
def positions():
    result = rh.get_open_stock_positions()
    ui.success(result)

@main.command(help='Returns a list of notifications.')
def notifications():
    result = rh.get_notifications()
    ui.success(result)
    
if __name__ == '__main__':
    main()