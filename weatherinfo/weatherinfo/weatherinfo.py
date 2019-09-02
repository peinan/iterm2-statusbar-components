import json
import traceback
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Union

import iterm2
import requests


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

    def __init__(self, tz='JST', hours=9):
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

    def iterm_format(self, use_icon=True, show_forecast=True) -> str:
        sep = '\uEB5E' if use_icon else '▶'
        th_char = '\uED0E ' if use_icon else ''
        unit = ''
        wc_char = f'{self.get_char(self.wci)} ' if use_icon else ''
        w3_char = f'{self.get_char(self.w3i)} ' if use_icon else ''

        weather_now = f'{wc_char}{self.wc} {th_char}{self.tcs}{unit}'
        forecast = f' {sep} {w3_char}{self.w3} {th_char}{self.t3s}{unit}'

        if show_forecast:
            text = weather_now + forecast
        else:
            text = weather_now

        return text


def is_refresh_time():
    now = datetime.now()
    return now.minute % 10 == 0


def have_log():
    return LOGFILE_PATH.exists()


def read_log():
    return json.load(LOGFILE_PATH.open())


def write_log(city: str, use_icon: bool, units: str, show_forecast: bool, weather_info: str):
    log_data = {
        'city': city,
        'use_icon': use_icon,
        'units': units,
        'show_forecast': show_forecast,
        'weather_info': weather_info
    }
    json.dump(log_data, LOGFILE_PATH.open('w'), ensure_ascii=False)


@dataclass
class KnobOption:
    name: str
    v: Union[str, bool]


CONFIG = json.load((Path(__file__).parent / 'config.json').open())
APIKEY = CONFIG['OpenWeatherAPIKey']
LOGFILE_PATH = Path('/tmp/iterm-weatherinfo.log')
w = WeatherInfo()
w.APIKEY = APIKEY


async def main(connection):
    knob_city = KnobOption('city', 'Shibuya')
    knob_use_icon = KnobOption('use_icon', True)
    knob_use_imperial = KnobOption('use_imperial', False)
    knob_show_forecast = KnobOption('show_forecast', True)
    knobs = [
        iterm2.StringKnob('City', knob_city.v, knob_city.v, knob_city.name),
        iterm2.CheckboxKnob('Use icon', knob_use_icon.v, knob_use_icon.name),
        iterm2.CheckboxKnob('Show forecast', knob_show_forecast.v, knob_show_forecast.name),
        iterm2.CheckboxKnob('Use imperial units', knob_use_imperial.v, knob_use_imperial.name),
    ]

    component = iterm2.StatusBarComponent(
        short_description='Weather Info',
        detailed_description='A component that will tell you the current weather and the forecast.',
        knobs=knobs,
        exemplar=' Clouds  27.1   Clear  27.1',
        update_cadence=60,
        identifier='peinan.weather'
    )

    def is_true_knob(knobs, knob_option: KnobOption):
        return bool(knob_option.name in knobs and knobs[knob_option.name])

    @iterm2.StatusBarRPC
    async def weather_info(knobs):
        w.CITYNAME = knobs[knob_city.name] if is_true_knob(knobs, knob_city) else 'Shibuya'
        w.UNITS = 'imperial' if is_true_knob(knobs, knob_use_imperial) else 'metric'
        use_icon = knobs[knob_use_icon.name] if is_true_knob(knobs, knob_use_icon) else False
        show_forecast = knobs[knob_show_forecast.name] if is_true_knob(knobs, knob_show_forecast) else False

        # print(w.CITYNAME, w.UNITS, use_icon, show_forecast)  # for debug

        if have_log():
            log_data = read_log()
            if not is_refresh_time() and (w.CITYNAME == log_data['city'] and w.UNITS == log_data['units'] and
               use_icon == log_data['use_icon'] and show_forecast == log_data['show_forecast']):
                return log_data['weather_info']

        print(f'[application info] Fetching weather: {knobs}')
        w.fetch_weather()
        w.parse_weather()
        weather_info = w.iterm_format(use_icon=use_icon, show_forecast=show_forecast)
        write_log(w.CITYNAME, use_icon, w.UNITS, show_forecast, weather_info)

        return weather_info

    await component.async_register(connection, weather_info)


iterm2.run_forever(main)
