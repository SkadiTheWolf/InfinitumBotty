"""

This module takes an City and Queries open-metero.com for a temperature, Weather Code And Pressure

January 2026, Skadi Wiesemann

"""

import requests
import json

from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype

code = {
    0: 'Klarer Himmel',
    1: 'Überwiegend Klarer Himmel',
    2: 'Partiell Bewölkt',
    3: 'Bewölkt',
    45: 'Nebel',
    48: 'Überfrierender Nebel',
    51: 'Leichter Nieselregen',
    53: 'Mittlerer Nieselregen',
    55: 'Schwerer Nieselregen',
    56: 'Leichter überfrierender  Nieselregen',
    57: 'Schwerer überfrierender  Nieselregen',
    61: 'Leichter Regen',
    63: 'Mitterer Regen',
    65: 'Schwerer Regen',
    66: 'Leichter frierender  Regen',
    67: 'Schwerer frierender  Regen',
    71: 'Leichter Schneefall',
    73: 'Mittlerer Schneefall',
    75: 'Schwerer Schneefall',
    77: 'Graupel',
    80: 'Leichter Regenschauer',
    81: 'Mittlerer Regenschauer',
    82: 'Schwerer Regenschauer',
    85: 'Leichtes Schneegestöber',
    86: 'Schweres Schneegestöber',
    95: 'Gewitter',
    96: 'Gewitter',
    99: 'Gewitter',
}

class WeatherObserver(PrivMsgObserverPrototype):


    @staticmethod
    def cmd():
        return ['.wetter']

    @staticmethod
    def help():
        return ['.wetter <Stadt> - Befragt open-meteo.com nach einer Temperatur, Wettercode und Luftdruck am spezifizierten Ort']

    def update_on_priv_msg(self, data, connection: Connection):
        # Hoisting of variables
        global lat
        global long
        global City
        global country
        global temperature

        if data['messageCaseSensitive'].find('.wetter') == -1:
            return

        # split incoming message in '<City>'
        message = str(data['messageCaseSensitive'])
        city = message.replace('.wetter ', '')
        city = city.replace(' ', '+')

        # Get Coordinates for Specified City
        url = f'https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json'
        contents = requests.get(url)
        status = contents.status_code

        if status == 200:
            data1 = json.loads(contents.content)
            try:
                dictLoc = data1['results'][0]
            except KeyError:
                connection.send_back("Stadt nicht Gefunden", data)
                return
            lat = dictLoc['latitude']
            long = dictLoc['longitude']
            City = dictLoc['name']
            country = dictLoc['country_code']

            # Get Weather info
            urlWeather = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&models=icon_seamless&current=weather_code,temperature_2m,surface_pressure&timezone=Europe%2FBerlin'
            contentsWeather = requests.get(urlWeather)
            statusWeather = contentsWeather.status_code

            if statusWeather == 200:
                dataWeather = json.loads(contentsWeather.content)
                dictWeather = dataWeather['current']
                temperature = dictWeather['temperature_2m']
                weather_code = dictWeather['weather_code']
                pressure = dictWeather['surface_pressure']

                connection.send_back(f'Die Temperatur in {City}, {country} beträgt im Moment {temperature} °C. Die Witterung ist {code[weather_code]}. Der Luftdruck beträgt {pressure} hPa', data)

            else:
                connection.send_back(f"Fehler: Get Temp: Statuscode:{status}", data)

        else:
            connection.send_back(f"Fehler: Get Coords: Statuscode:{status}", data)


