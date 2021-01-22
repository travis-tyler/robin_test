import click
import robin_stocks as rh
import ui
from config import user, pw

@click.group()
def main():
    rh.login(user, pw)

@main.command(help='Gets the information associated with the accounts profile being held by Robinhood.')
@click.option('--fetch', type=click.STRING)
def info(fetch):
    print(f'Fetching {fetch}....')
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
        ui.success(f"{quote['symbol']} | {quote['ask_price']}")


@main.command(help='Gets help for all stocks in your watchlist')
def watchlist():
    print('Getting quotes for watchlist....')
    
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
        ui.success(f'Bying {quantity} of {symbol} at market price....')
        result = rh.order_buy_market(symbol, quantity)

    ui.chec_ref(result)

@main.command(help='Sells quantity of stock by symbol')
@click.argument('quantity', type=click.INT)
@click.argument('symbol', type=click.STRING)
@click.option('--limit', type=click.FLOAT)
def sell(quantity, symbol, limit):
    if limit is not None:
        ui.success(f"Selling {quantity} of {symbol} at ${limit}")
        result = rh.order_sell_limit(symbol, quantity, limit)
    else:
        ui.success(f'Selling {quantity} of {symbol} at market price....')
        result = rh.order_sell_market(symbol, quantity)

    ui.chec_ref(result)

@main.command(help='Buys fractional shares by symbol')
@click.argument('amount', type=click.FLOAT)
@click.argument('symbol', type=click.STRING)
def buy_frac(amount, symbol):
    ui.success(f'Buying ${amount} of {symbol}....')
    result = rh.order_buy_fractional_by_price(symbol, amount)

    ui.chec_ref(result)

@main.command(help='Represents the historicl data for a stock.')
@click.argument('symbol', type=click.STRING)
@click.option('--interval', type=click.STRING)
@click.option('--span', type=click.STRING)
def history(symbol, interval, span):
    ui.success(f'Get {interval} stock historicals for {symbol} for the past {span}....')
    result = rh.get_stock_historicals(symbol, interval, span)

    for i in result:
        for x in i:
            ui.success(f'{x}: {i[x]}')
        ui.bar()

    # ui.success(result)

@main.command(help='Generates support and resistance data from stock history by symbol.')
@click.argument('symbol', type=click.STRING)
@click.option('--interval', type=click.STRING)
@click.option('--span', type=click.STRING)
def get_lines(symbol, interval, span):
    ui.success(f'Get {interval} stock historicals for {symbol} for the past {span}....')
    result = rh.get_stock_historicals(symbol, interval, span)

    hist = {'dates':[], 
            'lows':[], 
            'highs':[], 
            'opens':[], 
            'closes':[], 
            'volumes':[]}

    for i in result:
        hist['dates'].append(i['begins_at'][:10])
        hist['lows'].append(i['low_price'])
        hist['highs'].append(i['high_price'])
        hist['opens'].append(i['open_price'])
        hist['closes'].append(i['close_price'])
        hist['volumes'].append(i['volume'])

    ui.success(hist)




@main.command(help='Gets the information associated with the portfolios profile.')
def portfolio():
    print('Loading portfolio profile....')
    result = rh.load_portfolio_profile()

    ui.success(result)

@main.command(help='Gets the information associated with the portfolios profile.')
def investments():
    print('Loading investment profile....')
    result = rh.load_investment_profile()

    ui.success(result)
    
@main.command(help='Represents the historicl data for a stock.')
@click.argument('symbol', type=click.STRING)
def ratings(symbol):
    ui.success(f'Get stock ratings for {symbol}....')
    result = rh.get_ratings(symbol)

    ui.success(result)




if __name__ == '__main__':
    main()

