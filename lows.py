import pandas as pd

DEFAULT_THRESHOLD = 10

def getLows(df, threshold=DEFAULT_THRESHOLD):
    lows = []
    peak = df.iloc[0]['sp500']
    length = df.shape[0]
    last_row    = False
    last_record = {}
    for i in range(0, length):
        date    = df.iloc[i]['date']
        current = df.iloc[i]['sp500']
        if i == length - 1:
            last_row = True
            last_record = {'value':current, 'date':date}
        if current >= peak:
            peak = current
            if last_row:
                last_record['peak'] = True
        else:
            pc_down = 100 - ((current / peak) * 100)
            if last_row:
                last_record['% down from peak'] = round(pc_down,2)
                last_record['last peak'] = peak
            if pc_down > threshold:
                lows.append({'date': date, 'value': round(current, 2),  '% down': round(pc_down,2), 'from peak': peak})
                if last_row:
                    last_record['alert'] = True

    lows_df = pd.DataFrame(lows)
    lows_df.set_index('date', inplace=True)
    lows_df = lows_df.iloc[::-1]
    return lows_df, last_record
