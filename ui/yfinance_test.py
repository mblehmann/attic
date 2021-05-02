import time

import yfinance as yf

if __name__ == '__main__':
    # ticket = yf.Ticker('EVN.VI')

    begin = time.time()
    stocks = yf.Tickers('BG.VI CAI.VI EBS.VI EVN.VI LNZ.VI POST.VI OMV.VI RBI.VI SPI.VI UQA.VI VIG.VI')
    # stock = yf.Ticker('EVN.VI')  # 0.008867025375366211
    end = time.time()
    print(end - begin)

    print(dir(stocks))
    print(stocks.symbols)
    print(stocks.tickers)

    # get stock info
    # for key, value in ticket.info.items():
    #     print(key, value)

    # get historical market data
    # hist = ticket.history(period="max")
    # print(hist)

    # show actions (dividends, splits)
    # print(ticket.actions)

    # show dividends
    # print(ticket.dividends)

    # show splits
    # msft.splits

    # show financials
    # print(ticket.financials)
    # msft.quarterly_financials

    # show balance sheet
    # print(ticket.balance_sheet)
    # msft.quarterly_balance_sheet

    # show earnings
    # print(ticket.earnings)
    # msft.quarterly_earnings

    # show sustainability
    # print(ticket.sustainability)

    # # show analysts recommendations
    # msft.recommendations
    #
    # # show next event (earnings, etc)
    # print(ticket.calendar)

    # print(ticket.earnings)
    # print(ticket.balance_sheet)
    # print(ticket.balancesheet)
