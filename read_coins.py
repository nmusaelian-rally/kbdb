import pandas as pd

coins = ['burst','bitcoin','litecoin','nexus']

def getInitialOneYearDataDump(coin):
    '''
    this is done once
    '''
    # use coinmarketcap date format:
    start = '2017-01-01'.replace('-','')
    end   = '2017-12-31'.replace('-','')

    url = "https://coinmarketcap.com/currencies/%s/historical-data/?start=%s&end=%s" % (coin, start, end)
    df = pd.read_html(url, header=0)[0]
    df = df[::-1]
    csv_path = "data/%s.csv" % coin
    df.dropna().to_csv(csv_path, index=False)



def getCurrentCoinData(coin, start_date, end_date):
    start = start_date.replace('-','')
    end   =   end_date.replace('-','')
    url = "https://coinmarketcap.com/currencies/%s/historical-data/?start=%s&end=%s" % (coin, start, end)
    df = pd.read_html(url, header=0)[0]
    df.set_index('Date', inplace=True)
    df.rename(columns=lambda x: x.replace(' ', ''), inplace=True)
    df = df[::-1]
    return df

