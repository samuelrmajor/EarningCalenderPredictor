import time
import tools
Tickers = tools.getTickers()
count = -1
# Ignores ticker == A
for rawTicker in Tickers:
    try:
        ticker = rawTicker.strip()
        time.sleep(1)
        count += 1
        data = tools.requestAPI(ticker)
        tools.appendDf(data, ticker)
        tools.writeSuccess(count)
        print(ticker + " success: " + str(count))
    except:
        tools.writeFailure(count, ticker)
        print(ticker + " failure: " + str(count))
