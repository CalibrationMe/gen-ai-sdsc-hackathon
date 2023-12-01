from datetime import datetime, timedelta
import requests
import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry


from nixtlats import TimeGPT
import pandas as pd
from dotenv import load_dotenv

today = datetime.today().strftime('%Y-%m-%d')
wea_api_max_days = datetime.today() + timedelta(days=15)
wea_api_max_days = wea_api_max_days.strftime('%Y-%m-%d')
timegpt_max_days = datetime.today() + timedelta(days=160)
timegpt_max_days = timegpt_max_days.strftime('%Y-%m-%d')
print(today,wea_api_max_days,timegpt_max_days)

weather_pred_range = [today,wea_api_max_days]
timegpt_pred_range = [today,timegpt_max_days]
print(weather_pred_range,timegpt_pred_range)


# travel_start = "2023-12-03"
# travel_end = "2023-12-30"
# location_name='Zurich'

# test whether travel_start and travel_end are in the range of weather_pred_range
def test_date_range(travel_start,travel_end,weather_pred_range):
    if travel_start >= weather_pred_range[0] and travel_end <= weather_pred_range[1]:
        return True
    else:
        return False

# test whether travel_start and travel_end are in the range of timegpt_pred_range
def test_date_range(travel_start,travel_end,timegpt_pred_range):
    if travel_start >= timegpt_pred_range[0] and travel_end <= timegpt_pred_range[1]:
        return True
    else:
        return False
    
# print(test_date_range(travel_start,travel_end,weather_pred_range))

# print(test_date_range(travel_start,travel_end,timegpt_pred_range))


def get_hist4timegpt(date_str='2023-12-01',days_before=365,location_name='Zurich'):
    
    ## get st_day and end_day
    given_date = datetime.strptime(date_str, "%Y-%m-%d")
    last_day_of_previous_month = given_date - timedelta(days=days_before)
    st_day = last_day_of_previous_month.strftime("%Y-%m-%d")
    end_day = date_str

    
    # get location lon,lat
    url = f"https://geocode.maps.co/search?q={location_name}"
    response = requests.get(url)
    loc = response.json()
    lat, lon = (loc[0]['lat'],loc[0]['lon'])

    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": st_day,
        "end_date": end_day,
        "daily": ["temperature_2m_mean", "sunshine_duration", "precipitation_sum", "wind_speed_10m_max", "shortwave_radiation_sum"],
        "timezone": "Europe/Berlin"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    # print(f"Coordinates {response.Latitude()}°E {response.Longitude()}°N")
    # print(f"Elevation {response.Elevation()} m asl")
    # print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    # print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_temperature_2m_mean = daily.Variables(0).ValuesAsNumpy()
    daily_sunshine_duration = daily.Variables(1).ValuesAsNumpy()
    daily_precipitation_sum = daily.Variables(2).ValuesAsNumpy()
    daily_wind_speed_10m_max = daily.Variables(3).ValuesAsNumpy()
    daily_shortwave_radiation_sum = daily.Variables(4).ValuesAsNumpy()

    daily_data = {"date": pd.date_range(
        start = pd.to_datetime(daily.Time(), unit = "s"),
        end = pd.to_datetime(daily.TimeEnd(), unit = "s"),
        freq = pd.Timedelta(seconds = daily.Interval()),
        inclusive = "left"
    )}
    daily_data["temperature_2m_mean"] = daily_temperature_2m_mean
    daily_data["sunshine_duration"] = daily_sunshine_duration
    daily_data["precipitation_sum"] = daily_precipitation_sum
    daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
    daily_data["shortwave_radiation_sum"] = daily_shortwave_radiation_sum

    daily_dataframe = pd.DataFrame(data = daily_data)
    daily_dataframe.columns = ['date','temperature','sunshine_duration','precipitatio','wind_speed','shortwave_radiation']
    daily_dataframe['date'] = daily_dataframe['date'].dt.date
    daily_dataframe = daily_dataframe.dropna()
    daily_dataframe.sort_values(by='date', ascending=False, inplace=True)
 
    # print(daily_dataframe)
    daily_dataframe.to_csv('wea_data.csv',index=False)
    
    return daily_dataframe



def get_weaapi_pred(travel_start,travel_end,location_name):
    url = f"https://geocode.maps.co/search?q={location_name}"
    response = requests.get(url)
    loc = response.json()
    lat, lon = (loc[0]['lat'],loc[0]['lon'])


    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": ["temperature_2m_min", "sunshine_duration", "precipitation_sum", "wind_speed_10m_max", "shortwave_radiation_sum"],
        "timezone": "Europe/Berlin",
        "forecast_days": 16
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°E {response.Longitude()}°N")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_temperature_2m_min = daily.Variables(0).ValuesAsNumpy()
    daily_sunshine_duration = daily.Variables(1).ValuesAsNumpy()
    daily_precipitation_sum = daily.Variables(2).ValuesAsNumpy()
    daily_wind_speed_10m_max = daily.Variables(3).ValuesAsNumpy()
    daily_shortwave_radiation_sum = daily.Variables(4).ValuesAsNumpy()

    daily_data = {"date": pd.date_range(
        start = pd.to_datetime(daily.Time(), unit = "s"),
        end = pd.to_datetime(daily.TimeEnd(), unit = "s"),
        freq = pd.Timedelta(seconds = daily.Interval()),
        inclusive = "left"
    )}
    daily_data["temperature_2m_min"] = daily_temperature_2m_min
    daily_data["sunshine_duration"] = daily_sunshine_duration
    daily_data["precipitation_sum"] = daily_precipitation_sum
    daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
    daily_data["shortwave_radiation_sum"] = daily_shortwave_radiation_sum

    daily_dataframe = pd.DataFrame(data = daily_data)
    daily_dataframe.columns = ['date','temperature','sunshine_duration','precipitatio','wind_speed','shortwave_radiation']
    daily_dataframe['date'] = daily_dataframe['date'].dt.date
    daily_dataframe['date'] = daily_dataframe['date'].astype(str)

    # select data from travel period
    daily_dataframe = daily_dataframe[(daily_dataframe['date'] >= travel_start) & (daily_dataframe['date'] <= travel_end)]

    return daily_dataframe


def get_hist_wea_data(travel_start,travel_end,location_name):
    # Get today's date
    today = datetime.now().date()

    # Convert travel_end to datetime object
    travel_end_date = datetime.strptime(travel_end, "%Y-%m-%d").date()
    travel_start_date = datetime.strptime(travel_start, "%Y-%m-%d").date()
    # Initialize the nearest year as the current year
    nearest_year = today.year
    print(nearest_year)
    for year in range(today.year - 1, 0, -1):
        new_date = (datetime(year, travel_end_date.month, travel_end_date.day).date())
        if new_date < today:
            nearest_year = year
            break
    new_end_date= ((datetime(year, travel_end_date.month, travel_end_date.day).date()))

    # the same shift between new_end_date and travel_end_date is applied to travel_start_date
    new_start_date = travel_start_date + (new_end_date - travel_end_date)

    # change format to string
    new_start_date = new_start_date.strftime("%Y-%m-%d")
    new_end_date = new_end_date.strftime("%Y-%m-%d")
    print(new_start_date,new_end_date)



    # get location lon,lat
    url = f"https://geocode.maps.co/search?q={location_name}"
    response = requests.get(url)
    loc = response.json()
    lat, lon = (loc[0]['lat'],loc[0]['lon'])

    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": new_start_date,
        "end_date": new_end_date,
        "daily": ["temperature_2m_mean", "sunshine_duration", "precipitation_sum", "wind_speed_10m_max", "shortwave_radiation_sum"],
        "timezone": "Europe/Berlin"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°E {response.Longitude()}°N")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_temperature_2m_mean = daily.Variables(0).ValuesAsNumpy()
    daily_sunshine_duration = daily.Variables(1).ValuesAsNumpy()
    daily_precipitation_sum = daily.Variables(2).ValuesAsNumpy()
    daily_wind_speed_10m_max = daily.Variables(3).ValuesAsNumpy()
    daily_shortwave_radiation_sum = daily.Variables(4).ValuesAsNumpy()

    daily_data = {"date": pd.date_range(
        start = pd.to_datetime(daily.Time(), unit = "s"),
        end = pd.to_datetime(daily.TimeEnd(), unit = "s"),
        freq = pd.Timedelta(seconds = daily.Interval()),
        inclusive = "left"
    )}
    daily_data["temperature_2m_mean"] = daily_temperature_2m_mean
    daily_data["sunshine_duration"] = daily_sunshine_duration
    daily_data["precipitation_sum"] = daily_precipitation_sum
    daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
    daily_data["shortwave_radiation_sum"] = daily_shortwave_radiation_sum

    daily_dataframe = pd.DataFrame(data = daily_data)
    daily_dataframe.columns = ['date','temperature','sunshine_duration','precipitatio','wind_speed','shortwave_radiation']
    daily_dataframe['date'] = daily_dataframe['date'].dt.date
    daily_dataframe = daily_dataframe.dropna()
    daily_dataframe.sort_values(by='date', ascending=False, inplace=True)
 
    
    return daily_dataframe

def forcast_multi(key='hack.env', file='wea_data.csv', h=168, freq='D'):
    load_dotenv(key)
    timegpt = TimeGPT()
    timegpt.validate_token()

    df = pd.read_csv(file)
    df = df.rename(columns={'date': 'ds'})
    multi_df = pd.melt(df, id_vars=['ds'], var_name='unique_id', value_name='y')
    fcst_multi_df = timegpt.forecast(df=multi_df, h=h, model='timegpt-1-long-horizon', freq=freq)
    fcst_multi_dfnew = fcst_multi_df.pivot_table(values='TimeGPT', index='ds', columns='unique_id')
    fcst_multi_dfnew.to_csv('forcast.csv')
    return fcst_multi_df, fcst_multi_dfnew

def get_timegpt_pred(travel_start,travel_end,location_name):
        get_hist4timegpt(location_name = location_name)
        forcast_multi()
        df = pd.read_csv('forcast.csv')
        df = df.rename(columns={'ds': 'date'})
        # range from travel_start to travel_end
        df = df[(df['date'] >= travel_start) & (df['date'] <= travel_end)]
        return df

def get_wea_data_df(travel_start,travel_end,location_name):
    
    if test_date_range(travel_start,travel_end,weather_pred_range):
        print('weather api')
        # get data from weather api
        daily_dataframe = get_weaapi_pred(travel_start,travel_end,location_name)
    elif test_date_range(travel_start,travel_end,timegpt_pred_range):
        print('timegpt')
        # get data from timegpt
        daily_dataframe = get_timegpt_pred(travel_start,travel_end,location_name)
        print(daily_dataframe)
        # call timegpt to do the prediction
        #daily_dataframe = get_timegpt_pred(travel_start,travel_end,location_name)
    else:
        # use historical data
        print('hist')
        daily_dataframe = get_hist_wea_data(travel_start,travel_end,location_name)
        print(daily_dataframe)


# travel_start = "2023-12-03"
# travel_end = "2024-01-07"
# location_name='Zurich'
# get_wea_data_df(travel_start,travel_end,location_name)