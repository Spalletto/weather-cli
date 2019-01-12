from os.path import exists, expanduser
from re import match
from pytemperature import k2c
from datetime import datetime, timezone
import click
from requests import get
import pytz
import tzlocal

API_KEY = '2992a6f5340ee0ba7bd8e4e0ea4f62ad'

class ApiKey(click.ParamType):
    # class which determine as data type hexadecimal numbers in click
    name = 'api-key'

    def convert(self, value, param, ctx):
        found = match(r'[0-9a-f]{32}', value)

        if not found:
            self.fail(
                f"{value} is not a 32-character hexadecimal string",
                param,
                ctx,
            )

        return value


def current_weather(location, api_key=API_KEY):
    # get current weather from openweathermap site
    url = 'https://api.openweathermap.org/data/2.5/weather'

    query_params = {
        'q': location,
        'units': 'metric',
        'appid': api_key,
    }

    response = get(url, params=query_params)

    weather = {
        'description' : response.json()['weather'][0]['description'],
        'temperature' : response.json()['main']['temp'],
        'pressure' : response.json()['main']['pressure'],
        'humidity' : response.json()['main']['humidity'],
        'wind' : response.json()['wind'],
        'sunrise' : response.json()['sys']['sunrise'],
        'sunset' : response.json()['sys']['sunset'],
    }

    return weather

@click.group()
@click.option(
    '--api-key', '-a', 
    type=ApiKey(),
    help='your API key for the OpenWeatherMap API',
    metavar='<your-api-id>', 
)
@click.option(
    '--config-file', '-c',
    type=click.Path(),
    help='config file for storing OpenWeatherMap API key',
    metavar='<path>', 
    default='weather.cfg',
)
@click.pass_context
def main(ctx, api_key, config_file):
    """
    A little weather tool that shows you the current weather in a LOCATION of
    your choice. Provide the city name and optionally a two-digit country code.
    Here are two examples:\n
    1. Lviv,UA\n
    2. Kyiv\n
    You need a valid API key from OpenWeatherMap for the tool to work. You can
    sign up for a free account at https://openweathermap.org/appid.
    """

    # creating context with api-key and config file
    filename = expanduser(config_file)

    if not api_key and exists(filename):
        with open(filename) as cfg:
            api_key = cfg.read()

    ctx.obj = {
        'api_key': api_key,
        'config_file': filename,
    }

@main.command(options_metavar='<options>')
@click.pass_context
def config(ctx):
    """
    Store configuration values in a file, e.g. the API key for OpenWeatherMap.
    """
    config_file = ctx.obj['config_file']
    
    api_key = click.prompt(
        "Please enter your API key",
        default=ctx.obj.get('api_key', '')
    )

    with open(config_file, 'w') as cfg:
        cfg.write(api_key)

@main.command(options_metavar='<options>')
@click.argument('location', metavar='<location>')
@click.pass_context
def current(ctx, location):
    """
    Show the current weather for a location using OpenWeatherMap data.
    """
    api_key = ctx.obj['api_key']

    weather = current_weather(location, api_key)

    click.secho(f"The weather in {location} right now: {weather.get('description')}.\n", fg='bright_green', bold=True) 
    click.secho(f"Temperature:\t {weather.get('temperature')} °C", fg='green') 
    click.secho(f"Pressure:\t {weather.get('pressure')} mm", fg='green') 
    click.secho(f"Humidity:\t {weather.get('humidity')} %", fg='green') 
    click.secho(f"Wind:\t\t {weather.get('wind')['deg']} deg, {weather.get('wind')['speed']} m/s", fg='green') 
    click.secho(f"\nSunrise time:\t {datetime.utcfromtimestamp(weather.get('sunrise')).strftime('%H:%M:%S')} UTC", fg='green') 
    click.secho(f"Sunset time:\t {datetime.utcfromtimestamp(weather.get('sunset')).strftime('%H:%M:%S')} UTC", fg='green') 
    

if __name__ == "__main__":
    main()
