#!/usr/bin/env python3.5

import click
import requests

SAMPLE_API_KEY = '2992a6f5340ee0ba7bd8e4e0ea4f62ad'

def current_weather(location, api_key=SAMPLE_API_KEY):
    url = 'https://api.openweathermap.org/data/2.5/weather'

    query_params = {
        'q': location,
        'appid': api_key,
    }

    response = requests.get(url, params=query_params)

    return response.json()['weather'][0]['description']


@click.command(options_metavar='<options>')
@click.argument('location', metavar='<location>')
@click.option(
    '--api-key', '-a', 
    help='your API key for the OpenWeatherMap API',
    metavar='<your-api-id>'
)
def main(location, api_key):
    """
    A little weather tool that shows you the current weather in a LOCATION of
    your choice. Provide the city name and optionally a two-digit country code.
    Here are two examples:

    1. Lviv
    
    2. Kyiv  

    You need a valid API key from OpenWeatherMap for the tool to work. You can
    sign up for a free account at https://openweathermap.org/appid.
    """
    weather = current_weather(location, api_key)
    print("The weather in {location} right now: {weather}.".format(location=location, weather=weather)) 


if __name__ == "__main__":
    main()
