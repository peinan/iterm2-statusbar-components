import sys
from weatherinfo.weatherinfo import WeatherInfo

w = WeatherInfo()
w.APIKEY = sys.argv[1]
w.fetch_weather()
if w.fetch_status == 'SUCCEED':
    w.parse_weather()

w.print_weather_summary()

print()
print('=== iterm format ===')
print(w.iterm_format())
