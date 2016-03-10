from setuptools import setup

setup( name='strategy',
        version='0.1',
        description='Backtest moving average trading strategies',
        author='Albert DeFusco',
        license='MIT',
        packages=['strategy'],

        entry_points = {
            'scripts':'strategies = strategy.__main__:main'
            }

        )

