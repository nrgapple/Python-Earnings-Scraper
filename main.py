
import Stock
import operator


# Earnings Scraper Main:
all_stocks = []


run_save = input("(0) From save, (1) Run: ")

if run_save == 0:
    all_stocks = Stock.run_from_save()
elif run_save == 1:
    for i in xrange(0, 3):
        all_stocks += getAllStocks(i)
    save_file = open("stock_save.ag", 'wb')
    pickle.dump(all_stocks, save_file, -1)
    save_file.close()
else:
    print("Error: wrong input.")
all_stocks.sort(key=operator.attrgetter('difference'), reverse=True)
Stock.draw_table(all_stocks)

# for stock in all_stocks:
#     print (stock.__dict__.items())
