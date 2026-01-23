"""

This module takes an City and Queries open-metero.com for Weather Code

January 2026, Skadi Wiesemann

"""
import datetime

import requests
import json

from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype



class RainObserver(PrivMsgObserverPrototype):


    @staticmethod
    def cmd():
        return ['.rain']

    @staticmethod
    def help():
        return ['.rain <Stadt> - Befragt open-metero.com nach einem Wettercode am spezifizierten sort']

    def update_on_priv_msg(self, data, connection: Connection):
        # Hoisting of variables

        code = {
            0: 'Klarer Himmel',
            1: 'Überwiegend Klarer Himmel',
            2: 'Parziell Bewölkt',
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

        global lat
        global long
        global City
        global country


        if data['messageCaseSensitive'].find('.rain') == -1:
            return

        # split incoming message in '<City>'
        message = str(data['messageCaseSensitive'])
        city = message.replace('.rain ', '')
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
            urlWeather = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly=weather_code&models=icon_seamless&forecast_days=1'
            contentsWeather = requests.get(urlWeather)
            statusWeather = contentsWeather.status_code

            if statusWeather == 200:
                dataWeather = json.loads(contentsWeather.content)
                dictWeather = dataWeather['hourly']
                weatherCode = dictWeather['weather_code']
                jetzt = int(datetime.datetime.now().strftime('%H'))

                connection.send_back(f'Das Wetter in {City}, {country} ist im Moment {code[weatherCode[jetzt-1]]}', data)

            else:
                connection.send_back(f"Fehler: Get Temp: Statuscode:{statusWeather}", data)

        else:
            connection.send_back(f"Fehler: Get Coords: Statuscode:{status}", data)


