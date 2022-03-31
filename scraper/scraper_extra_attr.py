import tools
Tickers = tools.getTickers()
count = -1
# Ignores ticker == A
for rawTicker in Tickers:
    try:
        ticker = rawTicker.strip()
        count += 1
        dataList = tools.requestAPICombo(ticker)
        data = dataList[0]
        data2 = dataList[1]
        tools.appendDfCombo(data, data2, ticker)
        tools.writeSuccess(count)
        print(ticker + " success: " + str(count))
    except:
        tools.writeFailure(count, ticker)
        print(ticker + " failure: " + str(count))
