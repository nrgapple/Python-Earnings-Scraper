
## useful link for yahoo api.

from __future__ import print_function
import datetime
import money
import helper_functions
from lxml import html
import csv
import yahoo_finance
from texttable import Texttable
import pickle
import progressbar

# extra:
import requests


class Stock:
    count = 0

    def __init__(self):
        # string: name of stock.
        self.name = None
        # string: stock ticker symbol.
        self.ticker = None
        # projected EPS forcast. 
        self.EPS_forcast = None
        # last years EPS.
        self.EPS_last_year = None
        # date to release Earnings.
        self.earnings_date = None
        # Number of Estimates.
        self.estimates_count = None
        # Yahoo Reference
        self.Yahoo = None
        # current price.
        self.current_price = None
        # Forcast object for the Stock.
        self.forcast = None
        # Stock Exange
        self.exange = None
        # difference in EPS
        self.difference = None
        # # Stock asking price.
        # self.ask_price = None
        # # Stock current asking price.
        # self.current_ask_price = None
        # # Stock bid price.
        # self.open_price = None
        # # Stock previous close price.
        # self.prev_close_price = None
        

    def getChangeInEPS(self):
        if self.EPS_last_year and self.EPS_forcast:
            return self.EPS_forcast - self.EPS_last_year
        else:
            return None
class Forcast:
    
    def __init__(self):
        self.buy = None
        self.outperform = None
        self.hold = None
        self.underperform = None
        self.sell = None

def draw_table(all_stocks):
    t = Texttable()
    #t.add_rows(ERsorted)
    t.header(["ticker",
            "price",
            "EPS Date",
            "current EPS",
            "past EPS",
            "difference",
            "b",
            "o",
            "h",
            "u",
            "s"])
    for stock_i in all_stocks:
        t.add_row([stock_i.ticker, \
                    stock_i.current_price, \
                    stock_i.earnings_date, \
                    stock_i.EPS_forcast, \
                    stock_i.EPS_last_year, \
                    stock_i.getChangeInEPS(), \
                    stock_i.forcast.buy, \
                    stock_i.forcast.outperform, \
                    stock_i.forcast.hold, \
                    stock_i.forcast.underperform, \
                    stock_i.forcast.sell])

    t.set_cols_width([6, 6, 12, 12, 9, 11, 2, 2, 2, 2, 2])
    t.set_cols_align(["c","r","r","r","r","r","r","r","r","r","r"])

    print (t.draw())

def NAToNoneOrValue(_string):
    if _string == "N/A":
        return None
    else:
        return _string

# returns a string in format "APP+STL" for yahoo's api.
def makeYahooStockString(stockArr):
    yahoo_stock_string = ""
    for stock_inter in stockArr:
        yahoo_stock_string += stock_inter.ticker
        # not the last element.
        if stock_inter != stockArr[-1]:
            yahoo_stock_string += "+"
    return yahoo_stock_string



# takes in yahoo api symbols for different stock data 
# and an array of Stock objects.
# returns array of stock info.
def getYahooAPIDataArray(data_string, stockArr):
    yahoo_stock_string = makeYahooStockString(stockArr)
    yahoo_url = "http://finance.yahoo.com/d/quotes.csv?s=" + yahoo_stock_string + "&f=" + data_string

    with requests.Session() as s:
        download = s.get(yahoo_url)

        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        stock_data = list(cr)
    return stock_data


def setMarketsData(_all_stocks):
    print ("-Getting Markets Forcast Data")
    bar = progressbar.ProgressBar(max_value=len(_all_stocks))
    bar_i = 1
    for stock_i in _all_stocks:
        markets_page = requests.get('https://markets.ft.com/data/equities/tearsheet/forecasts?s=' + stock_i.ticker)
        markets_tree = html.fromstring(markets_page.content)
        forcast = markets_tree.xpath('/html/body/div[3]/div[2]/section[3]/div[1]/div/div/section[2]/div[2]/table/tbody//text()')
        stock_i.forcast = Forcast()
        if forcast:
            stock_i.forcast.buy = forcast[1]
            stock_i.forcast.outperform = forcast[3]
            stock_i.forcast.hold = forcast[5]
            stock_i.forcast.underperform = forcast[7]
            stock_i.forcast.sell = forcast[9]
        bar.update(bar_i)
        bar_i += 1

    print ("]")
def getAllStocks(day_offset):

    current_date = datetime.date.today() + datetime.timedelta(days=day_offset)

    nasdaq_page = requests.get('http://www.nasdaq.com/earnings/earnings-calendar.aspx?date=' + current_date.strftime("%Y-%B-%d"))
    nasdaq_tree = html.fromstring(nasdaq_page.content)

    temp_EPS_forcast = helper_functions.convert_to_float(nasdaq_tree.xpath('//*[@id="ECCompaniesTable"]/tr[position()>0]/td[5]//text()'))
    temp_EPS_last_year = helper_functions.convert_to_float(nasdaq_tree.xpath('//*[@id="ECCompaniesTable"]/tr[position()>0]/td[8]//text()'))
    temp_names = nasdaq_tree.xpath('//*[starts-with(@id,"two_column_main_content_CompanyTable_companyname_")]/text()')
    temp_tickers = helper_functions.convert_to_ticker(temp_names)

    all_stocks = []
    for i in xrange(len(temp_names)):
        temp_Stock = Stock()
        temp_Stock.name = temp_names[i]
        temp_Stock.ticker = temp_tickers[i]
        temp_Stock.EPS_forcast = temp_EPS_forcast[i]
        temp_Stock.EPS_last_year = temp_EPS_last_year[i]
        temp_Stock.earnings_date = current_date
        temp_Stock.difference = temp_Stock.getChangeInEPS();
        # Yahoo Stuff.
        temp_Stock.Yahoo = yahoo_finance.Share(temp_Stock.ticker)
        temp_Stock.current_price = temp_Stock.Yahoo.get_price()
        temp_Stock.exange = temp_Stock.Yahoo.get_stock_exchange()
        
        all_stocks.append(temp_Stock)

    #print (all_stocks[0].__dict__.items())

    setMarketsData(all_stocks)

    return all_stocks

def run_from_save():
    try:
        save_file = open('stock_save.ag', 'rb')
        all_stocks = pickle.load(save_file)
        save_file.close()
        return all_stocks
    except:
        print ("No Save file.")
        return None



