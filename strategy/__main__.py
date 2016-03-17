#!/usr/bin/env python
from strategy.movingaverage import MovingAverageCrossStrategy
from strategy.backtest import MarketOnClosePortfolio
import pandas as pd
from pandas_datareader import data

def main():
    apple = data.DataReader('AAPL', 'yahoo', '1990')

    averages = [(10,50), (30,100), (50, 200), (100, 400)]
    capital = 1e5
    n_shares = 100

    company = ('AAPL', apple)

    print('Moving Average Strategries for %s' % company[0])
    print("  Initial capital %f " % capital)
    print()
    print('%6s %6s %8s' % ('short', 'long', 'return'))
    for short, long in averages:
        mav = MovingAverageCrossStrategy(company[0], company[1], short, long)
        mav.make_signals()

        port = MarketOnClosePortfolio(company[0], company[1], capital, mav, n_shares)
        port.backtest_portfolio()
        print('%6d %6d %8.2f' % (short,long,port.score()))

if __name__ == '__main__':
    main()
