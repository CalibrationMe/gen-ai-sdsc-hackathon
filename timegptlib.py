from nixtlats import TimeGPT
import pandas as pd
from dotenv import load_dotenv

# This is the main forcasting function. h is the horizon times (number of data points).
# freq is in days (D), hours (H), months (M), etc...
# The function returns two sets of data, the original data in the correct format and the prediction


def forcast_multi(key='hack.env', file='wea_data.csv', h=10, freq='D', level=[10, 20]):
    load_dotenv(key)
    timegpt = TimeGPT()
    timegpt.validate_token()

    df = pd.read_csv(file)
    df = df.rename(columns={'date': 'ds'})
    multi_df = pd.melt(df, id_vars=['ds'], var_name='unique_id', value_name='y')
    fcst_multi_df = TimeGPT.forecast(df=multi_df, h=h, model='timegpt-1-long-horizon', freq=freq, level=level)
    fcst_multi_df.to_csv('forcast.csv')
    return multi_df, fcst_multi_df


# Use this funciton to plot your results. Make sure you enter the original data and the forcast data.
def plot(data, fcst_data, level=[10, 20]):
    TimeGPT.plot(data, fcst_data, time_col='ds', target_col='y', level=level)


if __name__ == '__main__':
    print('Hi')

