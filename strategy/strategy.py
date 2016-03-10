#!/usr/bin/env python

import pandas as pd
from pandas_datareader import data


class MovingAverageCrossStrategy(object):
    def __init__(self, symbol, bars, short_window, long_window):
        self.symbol = symbol
        self.bars = bars
        self.short_window = short_window
        self.long_window = long_window


    def make_signals(self):
        self.signals = pd.DataFrame(index = self.bars.index)
        self.signals['signal'] = 0

        self.signals['short_mavg'] = pd.rolling_mean(self.bars['Close'], window=self.short_window, min_periods=1)
        self.signals['long_mavg'] = pd.rolling_mean(self.bars['Close'], window=self.long_window, min_periods=1)

        def cross(x):
            short = x['short_mavg']
            long = x['long_mavg']
            if short > long:
                return 1
            else:
                return 0

        self.signals['signal'] = self.signals.iloc[self.short_window:].apply(cross, axis=1)

        self.signals['positions'] = self.signals['signal'].diff()


    def plot(self):
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15,8))

        ax.plot('Close', data=self.bars, color='gray', linewidth=2,
                label='Close')

        ax.plot('short_mavg', data=self.signals, color='green', linewidth=2,
                label='%d day moving average' % self.short_window)
        ax.plot('long_mavg', data=self.signals, color='blue', linewidth=2,
                label='%d day moving average' % self.long_window)

        buy=self.signals['positions'] == 1
        sell=self.signals['positions'] == -1

        ax.plot(self.signals.loc[buy].index, self.signals.loc[buy, 'short_mavg'], '^', color='black', label='',
               markersize=10)
        ax.plot(self.signals.loc[sell].index, self.signals.loc[sell, 'short_mavg'], 'v', color='red', label='',
               markersize=10)

        ax.set_title('Moving Average Cross Strategy: %s' % self.symbol)
        ax.set_ylabel('Price in US Dollars')

        ax.legend(loc=0)

        return fig

class MarketOnClosePortfolio(object):
    def __init__(self, symbol, bars, initial_capital, strategy, n_shares=100):
        self.symbol = symbol
        self.initial_capital = initial_capital
        self.n_shares = n_shares
        self.strategy = strategy
        self.bars = bars
        self.make_positions()


    def make_positions(self):
        self.positions = pd.DataFrame(index=self.strategy.signals.index).fillna(0.0)
        self.positions[self.symbol] = self.n_shares*self.strategy.signals['signal']

    def backtest_portfolio(self):
        self.portfolio = pd.DataFrame(index=self.bars.index)

        pos_diff = self.positions[self.symbol].diff()

        self.portfolio['holdings'] = (self.positions[self.symbol]*self.bars['Close'])
        self.portfolio['cash'] = self.initial_capital - (pos_diff*self.bars['Close']).cumsum()

        self.portfolio['total'] = self.portfolio['cash'] + self.portfolio['holdings']
        self.portfolio['returns'] = self.portfolio['total'].pct_change()

    def score(self):
        init=self.initial_capital
        final=self.portfolio['total'].iloc[-1]
        return (final-init)/init*100.

    def plot(self):
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15,8))

        ax.plot('total', data=self.portfolio, color='blue', linewidth=2)

        buy = self.strategy.signals.positions == 1
        sell = self.strategy.signals.positions == -1

        ax.plot(self.portfolio.loc[buy].index, self.portfolio.loc[buy, 'total'], '^', color='black', label='',
               markersize=10)
        ax.plot(self.portfolio.loc[sell].index, self.portfolio.loc[sell, 'total'], 'v', color='red', label='',
               markersize=10)

        return fig

if __name__ == '__main__':
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
