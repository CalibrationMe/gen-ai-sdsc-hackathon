from nixtlats import TimeGPT
import pandas as pd
from dotenv import load_dotenv

# This is the main forcasting function. h is the horizon times (number of data points).
# freq is in days (D), hours (H), months (M), etc...
# The function returns two sets of data, the original data in the correct format and the prediction


def forcast_multi(key='hack.env', file='wea_data.csv', h=10, freq='D', level=[10, 20], outputfile='filterForcast.csv'):
    load_dotenv(key)
    timegpt = TimeGPT()
    timegpt.validate_token()

    df = pd.read_csv(file)
    df = df.rename(columns={'date': 'ds'})
    multi_df = pd.melt(df, id_vars=['ds'], var_name='unique_id', value_name='y')
    fcst_multi_df = timegpt.forecast(df=multi_df, h=h, model='timegpt-1-long-horizon', freq=freq, level=level)
    fcst_multi_dfnew = fcst_multi_df.pivot_table(values='TimeGPT', index='ds', columns='unique_id')
    fcst_multi_dfnew.to_csv(outputfile)
    return fcst_multi_df, fcst_multi_dfnew


def filter_forcast(file='wea_data.csv', startDate=None, endDate=None, outputfile='filterForcast.csv'):
    df = pd.read_csv(file)
    df['timestamp'] = pd.to_datetime(df['date'])
    df['year'] = df['timestamp'].dt.year
    df['month'] = df['timestamp'].dt.month
    df['day'] = df['timestamp'].dt.day

    dfFiltered = df[(df['month'] >= int(startDate.split("-")[1])) &
                    (df['month'] <= int(endDate.split("-")[1])) &
                    (df['day'] >= int(startDate.split("-")[2])) &
                    (df['day'] <= int(endDate.split("-")[2]))]
    dfFiltered.to_csv(outputfile)

    return dfFiltered


def filter_forcast(file='wea_data.csv', startDate=None, endDate=None, outputfile='filterForcast.csv'):
    df = pd.read_csv(file)
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%dT%H:%M')
    df['year'] = df['timestamp'].dt.year
    df['month'] = df['timestamp'].dt.month
    df['day'] = df['timestamp'].dt.day

    dfFiltered = df[(df['month'] >= int(startDate.split("-")[1])) &
                    (df['month'] <= int(endDate.split("-")[1])) &
                    (df['day'] >= int(startDate.split("-")[2])) &
                    (df['day'] <= int(endDate.split("-")[2]))]
    dfFiltered.to_csv(outputfile)

    return dfFiltered




# Use this funciton to plot your results. Make sure you enter the original data and the forcast data.
def plot(data, fcst_data, level=[10, 20]):
    TimeGPT.plot(data, fcst_data, time_col='ds', target_col='y', level=level)


if __name__ == '__main__':
    print('Hi')

