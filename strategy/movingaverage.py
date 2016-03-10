import pandas as pd

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
