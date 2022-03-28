from itertools import count
import pandas as pd
import env
import requests
import datetime
check = input("ARE YOU SURE? Y for continue!")
key = env.apikey

if check == "Y":
    base2 = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="
    end2 = "&outputsize=full&apikey=" + key
    base = 'https://www.alphavantage.co/query?function=EARNINGS&symbol='
    end = '&apikey=' + key
    ticker = "A"

    url = base + ticker + end
    url2 = base2+ticker+end2
    print(url2)
    r = requests.get(url)
    r2 = requests.get(url2)
    data = r.json()["quarterlyEarnings"]
    data2 = r2.json()["Time Series (Daily)"]

    df = pd.DataFrame.from_records(data)
    df['symbol'] = ticker
    df['dayBeforeEndPrice'] = "test"
    df['dayAfterEndPrice'] = "test"
    df['dayBeforeVolume'] = "test"
    df['dayAfterVolume'] = "test"
    df = df.reset_index()
    validDates = data2.keys()
    for index, row in df.iterrows():
        dateRelease = datetime.datetime.strptime(
            row["reportedDate"], '%Y-%m-%d')
        # Ensures day before is a business day
        succesfulDateBefore = False
        counterSuccDateBefore = 0
        while not(succesfulDateBefore) or counterSuccDateBefore <= 10:
            counterSuccDateBefore += 1
            if str(dateRelease - datetime.timedelta(days=counterSuccDateBefore))[0:10] in validDates:
                dateBefore = str(
                    dateRelease - datetime.timedelta(days=counterSuccDateBefore))[0:10]
                succesfulDateBefore = True
                print(dateBefore)
                dayBeforeEndPrice = data2[dateBefore]["4. close"]
                dayBeforeEndVolume = data2[dateBefore]["5. volume"]
        if not(succesfulDateBefore):
            dayBeforeEndPrice = "NAN"
            dayBeforeEndVolume = "NAN"
        # Ensures day after is a business day
        succesfulDateAfter = False
        counterSuccDateAfter = 0
        while not(succesfulDateAfter) or counterSuccDateAfter <= 10:
            counterSuccDateAfter += 1
            if str(dateRelease + datetime.timedelta(days=counterSuccDateAfter))[0:10] in validDates:
                dateAfter = str(
                    dateRelease + datetime.timedelta(days=counterSuccDateAfter))[0:10]
                succesfulDateAfter = True
                dayAfterEndPrice = data2[dateAfter]["4. close"]
                dayAfterEndVolume = data2[dateAfter]["5. volume"]
        if not(succesfulDateAfter):
            dayAfterEndPrice = "NAN"
            dayAfterEndVolume = "NAN"
        dateRelease = str(dateRelease)[0:10]

        df.iat[index, df.columns.get_loc(
            'dayBeforeEndPrice')] = dayBeforeEndPrice
        df.iat[index, df.columns.get_loc(
            'dayBeforeVolume')] = dayBeforeEndVolume
        df.iat[index, df.columns.get_loc(
            'dayAfterEndPrice')] = dayAfterEndPrice
        df.iat[index, df.columns.get_loc(
            'dayAfterVolume')] = dayAfterEndVolume

    print(df)
    # df2 = pd.DataFrame.from_records(data2)

    # df.to_csv("data/output/historicEarningsAndPrices.csv", index=False)
else:
    print("Setup Aborted")
