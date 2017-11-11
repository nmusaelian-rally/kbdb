import pandas as pd


def timing(df):
    years = df.columns.tolist()
    methods = ['HoldStocks', 'HoldBonds', 'MarketTiming', 'BetterMarketTiming']

    loss_before_act = -10
    loss_before_act_late = -20

    before_bad = '2007'
    bad = '2008'
    good = '2009'

    tdata = []
    for method in methods:
        balance = 10000
        values = []
        for year in years:
            if method == 'HoldStocks':
                percent_change = df.loc['STOCKS'][year]
                balance = balance + balance * percent_change / 100
                values.append(round(balance, 2))
            elif method == 'HoldBonds':
                if year == before_bad:
                    percent_change = df.loc['STOCKS'][year]
                else:
                    if year == bad:
                        # balance adjusted for losses before investor acts
                        balance = balance + balance * loss_before_act / 100
                    percent_change = df.loc['BONDS'][year]
                balance = balance + balance * percent_change / 100
                values.append(round(balance, 2))
            elif method == 'MarketTiming':
                if year == bad or year == good:
                    if year == bad:
                        # balance adjusted for losses before investor acts
                        balance = balance + balance * loss_before_act_late / 100
                    # stay in bonds during bad and good year
                    percent_change = df.loc['BONDS'][year]
                else:
                    # switch to stocks after good year
                    percent_change = df.loc['STOCKS'][year]
                balance = balance + balance * percent_change / 100
                values.append(round(balance, 2))
            elif method == 'BetterMarketTiming':
                if year == bad:
                    # balance adjusted for losses before investor acts
                    balance = balance + balance * loss_before_act / 100
                    percent_change = df.loc['BONDS'][year]
                else:
                    percent_change = df.loc['STOCKS'][year]
                balance = balance + balance * percent_change / 100
                values.append(round(balance, 2))

        tdata.append(values)

    tdf = pd.DataFrame(tdata, index=methods, columns=years)
    return tdf

