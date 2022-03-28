# PE, before release value, after release value, %change, (beta (voliatility), delta, gamma) implied volitility, options are drastically? important in how volatile a stock maybe. Fucking with options?
import pandas as pd
Tickers = ['A', 'AA']
df = pd.read_csv('data/output/historicEarnings.csv')
print(df)
for ticker in Tickers:
    print(ticker)
