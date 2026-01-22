"""

This module takes a term and Queries Urban Dictionary for results. Prints the first one to the Chat

January 2026, Skadi Wiesemann

"""


import requests
import json

from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class WeatherObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".Weather"]

    @staticmethod
    def help():
        return ".Weather <Stadt> - Fragt open-metero.com nach der Temperatur an einem bestimmten Ort"

    def update_on_priv_msg(self, data, connection):

        # Hoisting of variables
        global lat
        global long
        global City
        global country
        global temperature


        if data['messageCaseSensitive'].find('.Weather') == -1:
            return

        #split incoming message in '<City>'
        message = str(data['messageCaseSensitive'])
        city = message.replace('.Weather', '')
        city = city.replace(' ', '+')

        #Get Coordinates for Specified City
        url = f'https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json'
        contents = requests.get(url)
        status = contents.status_code

        if status == 200:
            data = json.loads(contents.content)
            dictLoc = data['results'][0]
            lat = dictLoc['latitude']
            long = dictLoc['longitude']
            City = dictLoc['name']
            country = dictLoc['country_code']

        else:
            connection.send_back(f"Fehler: Get Coords: Statuscode:{status}", data)


            # Get Weather info
            urlWeather = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&models=icon_seamless&current=temperature_2m'
            contentsWeather = requests.get(urlWeather)
            statusWeather = contentsWeather.status_code

        if statusWeather == 200:
            dataWeather = json.loads(contents.content)
            dictWeather = dataWeather['current']
            temperature = dictWeather['temperature_2m']

            connection.send_back(f'Die Temperatur in {City}, {country} beträgt im Moment {temperature} °C', data)

        else:
            connection.send_back(f"Fehler: Get Temp: Statuscode:{status}", data)


