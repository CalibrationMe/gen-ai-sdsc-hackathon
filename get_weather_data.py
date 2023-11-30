from datetime import datetime, timedelta
import requests
import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry


def get_data(date_str='2023-11-20',days_before=30*5,location_name='Zurich'):
    
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



wea_data = get_data(date_str = '2023-11-30', location_name='Zurich')
wea_data.to_csv("wea_data.csv",index=False)