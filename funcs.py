import pandas as pd
import numpy as np
import json
import ui

def is_support(df, i):
    '''Determines if support line'''
    support = df['low'][i] < df['low'][i-1]\
        and df['low'][i] < df['low'][i+1]\
        and df['low'][i+1] < df['low'][i+2]\
        and df['low'][i-1] < df['low'][i-2]
    return support

def is_resistance(df, i):
    '''Determines if resistance line'''
    resistance = df['high'][i] > df['high'][i-1]\
        and df['high'][i] > df['high'][i+1]\
        and df['high'][i+1] > df['high'][i+2]\
        and df['high'][i-1] > df['high'][i-2]
    return resistance

def make_df(result):
    '''Creates and returns dataframe using pandas'''
    hist = {'date':[], 
        'low':[], 
        'high':[], 
        'open':[], 
        'close':[], 
        'volume':[]}

    for i in result:
        hist['date'].append(i['begins_at'][:10])
        hist['low'].append(i['low_price'])
        hist['high'].append(i['high_price'])
        hist['open'].append(i['open_price'])
        hist['close'].append(i['close_price'])
        hist['volume'].append(i['volume'])

    df = pd.DataFrame(hist)
    df['date'] = pd.to_datetime(df['date'])
    cols = df.columns.drop('date')
    df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')

    with open('data.txt', 'w') as outfile:
        json.dump(hist, outfile)

    return df

def get_s_r(df):
    '''Loops through DF to determine and return clear support and resistance lines'''
    s = np.mean(df['high'] - df['low'])

    levels = [] 

    for i in range(2, df.shape[0]-2):
        if is_support(df, i):
            l = df['low'][i]

            if np.sum([abs(l-x) < s for x in levels]) == 0:
                levels.append((i, l))
                ui.success(f'{l} | SUPPORT')

        elif is_resistance(df, i):
            l = df['high'][i]

            if np.sum([abs(l-x) < s for x in levels]) == 0:
                levels.append((i, l))

                ui.error(f'{l} | RESISTANCE')

    # return levels