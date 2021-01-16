import click
import robin_stocks as rh
import ui
from config import user, pw

@click.group()
def main():
    print('Logging in....')
    # rh.login(user, pw)

@main.command(help='Gets a stock quote for one or more symbols')
@click. argument('symbols', nargs=-1)
def quote(symbols):
    rh.login(user, pw)

    quotes = rh.get_quotes(symbols)

    for quote in quotes:
        ui.success(f"{quote['symbol']} | {quote['ask_price']}")


@main.command(help='Gets help for all stocks in your watchlist')
def watchlist():
    print('Getting quotes for watchlist...')
    
    with open('watchlist') as f:
        symbols = f.read().splitlines()

    quotes = rh.get_quotes(symbols)

    for quote in quotes:
        ui.success(quote)

@main.command(help='Buys quantity of stock by symbol')
@click.argument('quantity', type=click.INT)
@click.argument('symbol', type=click.STRING)
@click.option('--limit', type=click.FLOAT)
def buy(quantity, symbol, limit):
    if limit is not None:
        ui.success(f"Bying {quantity} of {symbol} at ${limit}")
        result = rh.order_buy_limit(symbol, quantity, limit)
    else:
        ui.success(f"Bying {quantity} of {symbol} at market price")
        result = rh.order_buy_market(symbol, quantity)

    if 'ref_id' in result:
        ui.success(result)
    else:
        ui.error(result)

@click.command(help='Sells quantity of stock by symbol')
@click.argument('quantity', type=click.INT)
@click.argument('symbol', type=click.STRING)
@click.option('--limit', type=click.FLOAT)
def sell(quantity, symbol, limit):
    if limit is not None:
        ui.success(f"Selling {quantity} of {symbol} at ${limit}")
        result = rh.order_sell_limit(symbol, quantity, limit)
    else:
        ui.success(f"Selling {quantity} of {symbol} at market price")
        result = rh.order_sell_market(symbol, quantity)

    if 'ref_id' in result:
        ui.success(result)
    else:
        ui.error(result)





    
if __name__ == '__main__':
    main()

