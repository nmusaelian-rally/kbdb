import pandas as pd

#snp500dump = pd.read_csv('data/snp500dump.csv')
#print (snp500dump.shape[0])

DEFAULT_THRESHOLD = 15

def getLows(d, threshold=DEFAULT_THRESHOLD):
    lows = []
    peak = d.iloc[0]['sp500']
    for i in range(0, len(d)):
        date    = d.iloc[i]['date']
        current = d.iloc[i]['sp500']
        if current >= peak:
            peak = current
        else:
            pc_down = 100 - ((current / peak) * 100)
            if pc_down > threshold:
                lows.append({'date': date, 'value': round(current, 2),  'pcdown': round(pc_down,2), 'from': peak})

    bad = pd.DataFrame(lows)
    return bad

# threshold = 14.00
# bad = getLows(snp500dump, threshold)
# print (bad)