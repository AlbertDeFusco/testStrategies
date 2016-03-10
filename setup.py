from setuptools import setup

setup( name='strategy',
        version='0.1',
        description='Backtest moving average trading strategies',
        author='Albert DeFusco',
        license='MIT',
        packages=['strategy'],

        package_data= {
            'strategy.tests' : ['data/*']
            },

        entry_points = {
            'scripts':'strategies = strategy.__main__:main'
            }

        )

