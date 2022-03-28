import env
import requests
import pandas as pd


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


def requestAPI(ticker):
    key = env.apikey
    base = 'https://www.alphavantage.co/query?function=EARNINGS&symbol='
    end = '&apikey=' + key
    url = base+ticker+end
    r = requests.get(url)
    data = r.json()["quarterlyEarnings"]
    return data


def getTickers():
    tickersFile = open('data/input/tickers.txt', 'r')
    uncleanTickers = tickersFile.readlines()
    return uncleanTickers


def test():
    print("test")
