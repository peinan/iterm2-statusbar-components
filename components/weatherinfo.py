import sys
from pathlib import Path

import iterm2

REAL_ROOTDIR_PATH = Path(__file__).resolve().parent
sys.path.append(REAL_ROOTDIR_PATH.__str__())

from lib.weatherinfo import WeatherInfo
from lib.utils import expand_path
from datetime import datetime
import json


CONFIG = json.load(open(REAL_ROOTDIR_PATH / 'config.json'))
APIKEY = CONFIG['OpenWeatherAPIKey']
LOGFILE_PATH = Path('/tmp/iterm-weatherinfo.log')
w = WeatherInfo(expand_path(CONFIG['PipPackagePath']))
w.APIKEY = APIKEY


def is_right_time():
    now = datetime.now()
    return now.minute % 10 == 0


def have_log():
    return LOGFILE_PATH.exists()


def read_log():
    return LOGFILE_PATH.open().readline()


def write_log(text):
    with LOGFILE_PATH.open('w') as f:
        f.write(text)


async def main(connection):
    component = iterm2.StatusBarComponent(
        short_description='Weather Info',
        detailed_description='A component that will tell you the current weather and the forecast.',
        knobs=[],
        exemplar=' Clouds  27.1   Clear  27.1',
        update_cadence=60,
        identifier='peinan.weather'
    )

    @iterm2.StatusBarRPC
    async def weather_info(knobs):
        if not is_right_time() and have_log():
            return read_log()

        print('[application info] Fetching weather')
        w.fetch_weather()
        w.parse_weather()
        weather_info = w.iterm_format()
        write_log(weather_info)

        return weather_info

    await component.async_register(connection, weather_info)


iterm2.run_forever(main)
