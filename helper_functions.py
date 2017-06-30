#!/usr/local/env python

# To make execututable:
# pyinstaller.exe --onefile scrape_test.py

from __future__ import print_function

from operator import itemgetter
from texttable import Texttable



import re
import readline
import json
import os.path
import npyscreen



def convert_string_to_markets(market):
    if market.startswith('NYSE'):
        return "NYQ"
    elif market.startswith('NasdaqGS'):
        return "NSQ"
    elif market.startswith('NasdaqCM'):
        return "NAQ"
    else:
        return "No"

def convert_to_float(number_list):
    floats = []
    for i in xrange(len(number_list)):
        temp = map(float, re.findall(r'[+-]?[0-9.]+', number_list[i]))
        if temp:
            floats.append(temp[0])
        else:
            floats.append(None)
    return floats

def convert_string_to_float(_string):
    temp = map(float, re.findall(r'[+-]?[0-9.]+', _string))
    if temp:
        return temp
    else:
        return None

def convert_to_ticker(ticker_list):
    tickers = []
    for i in xrange(len(ticker_list)):
        temp = ticker_list[i][ticker_list[i].find("(")+1:ticker_list[i].find(")")]
        tickers.append(temp)
    return tickers

def save_data(x,d):
    s = d.strftime('%Y-%B-%d')
    with open('save/save.ag', 'w') as outfile:
        json.dump(x, outfile)
    with open('save/last_save.ag', 'w') as f:
        json.dump(s,f)
    return

def load_data():
    with open('save/save.ag', 'r') as infile:
        x = json.load(infile)
    return x

def check_save_date():
    if os.path.isfile('save/last_save.ag'):
        with open('save/last_save.ag', 'r') as f:
            d = json.load(f)
        return d
    else:
        return 0


def set_weight(x):
    x['weight'] = float(x['percent change']) * .20 + \
                  float(x['buy']) * .20 + \
                  float(x['outperform']) * .10 + \
                  float(x['hold']) * -.05 + \
                  float(x['underperform']) * -.10 + \
                  float(x['sell']) * -.20
    return

def draw_table(all_stocks):
    t = Texttable()
    #t.add_rows(ERsorted)
    t.header(["ticker",
            "price",
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
                    stock_i.EPS_forcast, \
                    stock_i.EPS_last_year, \
                    stock_i.getChangeInEPS(), \
                    stock_i.forcast.buy, \
                    stock_i.forcast.overperform, \
                    stock_i.forcast.hold, \
                    stock_i.forcast.underperform, \
                    stock_i.forcast.sell])

    t.set_cols_width([6, 6, 12, 9, 11, 2, 2, 2, 2, 2])
    t.set_cols_align(["c","r","r","r","r","r","r","r","r","r"])

    print (t.draw())

#----------------------------------------------------------------------------





#print ('tickers: ', tickers)
#print ('ticker links:', ticker_links)

#print ('ticker dictionary:', ticker_dictionary)

#//*[@id="yfs_l84_adn.l"]

#*[@id="ECCompaniesTable"]/tbody/tr[24]/td[8]
