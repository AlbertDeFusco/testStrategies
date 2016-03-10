import pandas as pd

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

