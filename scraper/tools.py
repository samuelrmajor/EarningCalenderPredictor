import env
import requests
import pandas as pd
import time
import datetime


def writeFailure(count, ticker):
    file_object = open('data/output/failureIndex.txt', 'a')
    file_object.write(str(count) + " " + ticker + "\n")
    file_object.close()


def writeSuccess(count):
    file_object = open('data/output/successIndex.txt', 'a')
    file_object.write(str(count)+"\n")
    file_object.close()


def appendDf(data, ticker):
    outfile = "data/output/historicEarnings.csv"
    df = pd.DataFrame.from_records(data)
    df['symbol'] = ticker
    df.to_csv(outfile, mode="a", index=False, header=False)
    df.iloc[0:0]


def appendDfCombo(data, data2, ticker):
    outfile = "data/output/historicEarningsAndPrices.csv"
    df = pd.DataFrame.from_records(data)
    df['symbol'] = ticker
    df['dayBeforeEndPrice'] = 0
    df['dayAfterEndPrice'] = 0
    df['dayBeforeVolume'] = 0
    df['dayAfterVolume'] = 0
    validDates = data2.keys()
    for index, row in df.iterrows():
        dateRelease = datetime.datetime.strptime(
            row["reportedDate"], '%Y-%m-%d')
        # Ensures day before is a business day
        succesfulDateBefore = False
        counterSuccDateBefore = 0
        while not(succesfulDateBefore) and counterSuccDateBefore <= 10:
            counterSuccDateBefore += 1
            if str(dateRelease - datetime.timedelta(days=counterSuccDateBefore))[0:10] in validDates:
                dateBefore = str(
                    dateRelease - datetime.timedelta(days=counterSuccDateBefore))[0:10]
                succesfulDateBefore = True
                dayBeforeEndPrice = data2[dateBefore]["4. close"]
                dayBeforeEndVolume = data2[dateBefore]["5. volume"]
        if not(succesfulDateBefore):
            dayBeforeEndPrice = -1
            dayBeforeEndVolume = -1
        # Ensures day after is a business day
        succesfulDateAfter = False
        counterSuccDateAfter = 0
        while not(succesfulDateAfter) and counterSuccDateAfter <= 10:
            counterSuccDateAfter += 1
            if str(dateRelease + datetime.timedelta(days=counterSuccDateAfter))[0:10] in validDates:
                dateAfter = str(
                    dateRelease + datetime.timedelta(days=counterSuccDateAfter))[0:10]
                succesfulDateAfter = True
                dayAfterEndPrice = data2[dateAfter]["4. close"]
                dayAfterEndVolume = data2[dateAfter]["5. volume"]
        if not(succesfulDateAfter):
            dayAfterEndPrice = -1
            dayAfterEndVolume = -1
        dateRelease = str(dateRelease)[0:10]

        df.iat[index, df.columns.get_loc(
            'dayBeforeEndPrice')] = float(dayBeforeEndPrice)
        df.iat[index, df.columns.get_loc(
            'dayBeforeVolume')] = float(dayBeforeEndVolume)
        df.iat[index, df.columns.get_loc(
            'dayAfterEndPrice')] = float(dayAfterEndPrice)
        df.iat[index, df.columns.get_loc(
            'dayAfterVolume')] = float(dayAfterEndVolume)

    df.to_csv(outfile, mode="a", index=False, header=False)
    df.iloc[0:0]

# Gets all historic release dates


def requestAPI(ticker):
    key = env.apikey
    base = 'https://www.alphavantage.co/query?function=EARNINGS&symbol='
    end = '&apikey=' + key
    url = base+ticker+end
    r = requests.get(url)
    data = r.json()["quarterlyEarnings"]
    return data

# Gets historic release dates and combines them with stock performance information


def requestAPICombo(ticker):
    key = env.apikey
    base = 'https://www.alphavantage.co/query?function=EARNINGS&symbol='
    end = '&apikey=' + key

    base2 = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="
    end2 = "&outputsize=full&apikey=" + key

    url = base+ticker+end
    url2 = base2+ticker+end2

    r = requests.get(url)
    time.sleep(1)
    r2 = requests.get(url2)
    time.sleep(1)

    data = r.json()["quarterlyEarnings"]
    data2 = r2.json()["Time Series (Daily)"]

    return [data, data2]


def getTickers():
    tickersFile = open('data/input/tickers.txt', 'r')
    uncleanTickers = tickersFile.readlines()
    return uncleanTickers


def test():
    print("test")
