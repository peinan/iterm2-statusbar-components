import traceback
from datetime import datetime, timedelta, timezone


class WeatherInfo:

    APIKEY = ''
    CITYNAME = 'Shibuya'
    UNITS = 'metric'  # available units: metric, standard, imperial
    ENDPOINT = 'https://api.openweathermap.org/data/2.5'
    CURRENT_WEATHER_URL = '/weather'
    FORECAST_URL = '/forecast'

    ICON2CHAR = {
        '01': '\uED98',
        '02': '\uED94',
        '03': '\uED8F',
        '04': '\uED96',
        '09': '\uED95',
        '10': '\uED95',
        '11': '\uED92',
        '13': '\uED97',
        '50': '\uED90',
    }
    NA = 'N/A'

    def __init__(self, pip_package_path: str, tz='JST', hours=9):
        self.pip_package_path = pip_package_path
        self.tz = timezone(timedelta(hours=hours), tz)
        self.current_weather = None
        self.forecast_weather = None
        self.fetch_status = None

        self.lat = f'{self.NA}'
        self.lon = f'{self.NA}'
        self.dt  = f'{self.NA}'
        self.wc  = f'{self.NA}'
        self.wcd = f'{self.NA}'
        self.wci = f'02d'
        self.tc  = f'{self.NA}'
        self.tcs = f'{self.NA}'
        self.w3  = f'{self.NA}'
        self.w3d = f'{self.NA}'
        self.w3i = f'02d'
        self.t3  = f'{self.NA}'
        self.t3s = f'{self.NA}'

    def build_url(self, mode='current') -> str:
        if mode == 'current':
            url = f'{self.ENDPOINT}{self.CURRENT_WEATHER_URL}'
        elif mode == 'forecast':
            url = f'{self.ENDPOINT}{self.FORECAST_URL}'
        else:
            raise ValueError(f'Invalid mode={mode}: choose from `current` or `forecast`.')

        return url

    def build_params(self) -> dict:
        return {
            'q': self.CITYNAME,
            'APPID': self.APIKEY,
            'units': self.UNITS
        }

    def fetch_weather(self):
        import sys
        sys.path.append(self.pip_package_path)
        import requests

        self.current_weather = requests.get(self.build_url('current'), params=self.build_params())
        self.forecast_weather = requests.get(self.build_url('forecast'), params=self.build_params())

        if self.current_weather.status_code != 200 or self.forecast_weather.status_code != 200:
            self.fetch_status = 'FAILED'
        else:
            self.fetch_status = 'SUCCEED'

    def parse_weather(self):
        try:
            self.current_weather = self.current_weather.json()
            self.forecast_weather = self.forecast_weather.json()

            self.lat = self.current_weather['coord']['lat']
            self.lon = self.current_weather['coord']['lon']
            self.dt = datetime.fromtimestamp(self.current_weather['dt'], self.tz)
            self.wc = f"{self.current_weather['weather'][0]['main']}"
            self.wcd = f"{self.current_weather['weather'][0]['description']}"
            self.wci = self.current_weather['weather'][0]['icon']
            self.tc = self.current_weather['main']['temp']
            self.tcs = f'{self.tc:.1f}'
            self.w3 = f"{self.forecast_weather['list'][0]['weather'][0]['main']}"
            self.w3d = f"{self.forecast_weather['list'][0]['weather'][0]['description']}"
            self.w3i = self.forecast_weather['list'][0]['weather'][0]['icon']
            self.t3 = self.forecast_weather['list'][0]['main']['temp']
            self.t3s = f'{self.t3:.1f}'
        except:
            print(f'[ERROR] Something goes wrong: {traceback.format_exc()}')

    def get_char(self, icon: str) -> str:
        icon = icon[:2]
        if icon not in self.ICON2CHAR:
            return self.NA

        return self.ICON2CHAR[icon]

    def print_weather_summary(self):
        print(f'Fetch Status: {self.fetch_status}')
        print(f'City: {self.CITYNAME} ({self.lat}, {self.lon})')
        print()
        print('=== weather info ===')
        print(f'Datetime: {self.dt}')
        print(f'Current Weather: {self.get_char(self.wci)}  {self.wc} - {self.wcd}')
        print(f'Current Temperature: \uED0E  {self.tc}')
        print(f'3hrs Weather: {self.get_char(self.w3i)}  {self.w3} - {self.w3d}')
        print(f'3hrs Temperature: \uED0E  {self.t3}')

    def iterm_format(self) -> str:
        sep = '\uEB5E'
        th_char = '\uED0E'
        unit = ''
        wc_char = self.get_char(self.wci)
        w3_char = self.get_char(self.w3i)
        text = f'{wc_char} {self.wc} {th_char} {self.tcs}{unit}'\
               f' {sep} '\
               f'{w3_char} {self.w3} {th_char} {self.t3s}{unit}'

        return text


if __name__ == "__main__":
    import sys

    # run this directly like `$ python lib/weatherinfo.py` for the test if you need.
    w = WeatherInfo()
    w.APIKEY = sys.argv[1]
    w.fetch_weather()
    if w.fetch_status == 'SUCCEED':
        w.parse_weather()

    w.print_weather_summary()

    print()
    print('=== iterm format ===')
    print(w.iterm_format())
