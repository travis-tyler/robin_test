import click, json, robin_stocks as rh
import ui, funcs, config

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
    ui.success(f'\nGet {interval} stock historicals for {symbol} for the past {span}....\n')
    result = rh.get_stock_historicals(symbol, interval, span)

    for i in result:
        for x in i:
            ui.success(f'{x}: {i[x]}')
        ui.bar()

@main.command(help='Generates support and resistance data from stock history by symbol.')
@click.argument('symbol', type=click.STRING)
@click.option('--interval', type=click.STRING)
@click.option('--span', type=click.STRING)
def get_lines(symbol, interval, span):
    ui.success(f'\nGetting {interval} stock historicals for {symbol} for the past {span}....\n')
    result = rh.get_stock_historicals(symbol, interval, span)

    price = rh.get_quotes(symbol)[0]['last_extended_hours_trade_price']

    ui.bar()
    ui.success(f"Value: {price}")
    ui.bar()
    df = funcs.make_df(result)
    funcs.get_s_r(df)
    ui.bar()

    # with open('data.txt', 'w') as outfile:
    #     json.dump(result, outfile)

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

if __name__ == '__main__':
    main()