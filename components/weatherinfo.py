import json
import traceback
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Union
from urllib import request as urlreq, parse as urlparse
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import iterm2


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
        params = self.build_params()

        if mode == 'current':
            url = f'{self.ENDPOINT}{self.CURRENT_WEATHER_URL}?{urlparse.urlencode(params)}'
        elif mode == 'forecast':
            url = f'{self.ENDPOINT}{self.FORECAST_URL}?{urlparse.urlencode(params)}'
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
        try:
            with urlreq.urlopen(urlreq.Request(self.build_url('current'))) as res:
                self.current_weather = json.load(res)
            with urlreq.urlopen(urlreq.Request(self.build_url('forecast'))) as res:
                self.forecast_weather = json.load(res)
            self.fetch_status = 'SUCCEEDED'
        except:
            print(f'[ERROR] Fetch failed: {traceback.format_exc()}')
            self.fetch_status = 'FAILED'

    def parse_weather(self):
        try:
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


@dataclass
class KnobOption:
    name: str
    v: Union[str, bool]


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
        exemplar=' Clouds  27.1   Clear  30.2',
        update_cadence=60,
        identifier='peinan.weather'
    )

    def have_log():
        return LOGFILE_PATH.exists()

    def is_refresh_time():
        return datetime.now().minute % 10 == 0

    def is_opt_modify(knobs):
        opt_set = { k.name for k in [knob_city, knob_use_icon, knob_use_imperial, knob_show_forecast] }
        if set(knobs.keys()) & opt_set == opt_set:
            return True
        return False

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

    def knob_value(knobs, option: KnobOption, default_value):
        """returns the option's value if the option is in the knob, otherwise returns False"""
        return knobs[option.name] if option.name in knobs else default_value

    @iterm2.StatusBarRPC
    async def weather_info(knobs):
        w.CITYNAME = knob_value(knobs, knob_city, 'Shibuya')
        w.UNITS = 'imperial' if knob_value(knobs, knob_use_imperial, False) else 'metric'
        use_icon = bool(knob_value(knobs, knob_use_icon, True))
        show_forecast = bool(knob_value(knobs, knob_show_forecast, True))

        ## for debug
        # print(f'knobs: {knobs}')
        # print(f'have log file: {have_log()}, is refresh time: {is_refresh_time()}')

        if have_log():
            log_data = read_log()
            opt_req = is_opt_modify(knobs)
            is_same_opt = w.CITYNAME == log_data['city'] and w.UNITS == log_data['units'] and \
                          use_icon == log_data['use_icon'] and show_forecast == log_data['show_forecast']

            # print(f'is knob option request: {opt_req}, is same knob options: {is_same_opt}')

            if not opt_req or (is_same_opt and not is_refresh_time()):
                # print(f'[application info] Use stored weather info: '
                #       f'city={w.CITYNAME}, units={w.UNITS}, use_icon={use_icon}, show_forecast={show_forecast}')
                return log_data['weather_info']

        print(f'[application info] Fetching weather: {knobs}')
        w.fetch_weather()
        w.parse_weather()
        weather_info = w.iterm_format(use_icon=use_icon, show_forecast=show_forecast)
        write_log(w.CITYNAME, use_icon, w.UNITS, show_forecast, weather_info)

        return weather_info

    await component.async_register(connection, weather_info)


CONFIG = json.load((Path(__file__).parent / 'config.json').open())
APIKEY = CONFIG['OpenWeatherAPIKey']
LOGFILE_PATH = Path('/tmp/iterm-weatherinfo.log')
w = WeatherInfo()
w.APIKEY = APIKEY


iterm2.run_forever(main)
