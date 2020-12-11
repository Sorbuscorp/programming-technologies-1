import requests
from threading import Thread
import time
from datetime import datetime
from Database import Database

class VisualCrossingWeatherProvider:
    def __init__(self):
        self.key = "373QC5VVYP15RYE4BWGAIXRXY"

    def get(self, location, start_date, end_date):
        url = 'https://weather.VisualCrossingWebServices.com/VisualCrossingWebServices/rest/services/weatherdata/history'
        params = {
            'aggregateHours': 24,
            'startDateTime': f'{start_date}T00:0:00',
            'endDateTime': f'{end_date}T23:59:59',
            'unitGroup': 'metric',
            'location': location,
            'key': self.key,
            'contentType': 'json',
        }
        data = requests.get(url, params).json()
        return [
            {
                'date': row['datetimeStr'][:10],
                'mint': row['mint'],
                'maxt': row['maxt'],
                'location': 'Volgograd,Russia',
                'humidity': row['humidity'],
            }
            for row in data['locations'][location]['values']
        ]

class OpenWeatherProvider:
    def __init__(self):
        self.key = "64caf46dd0c4c7b007b0e64b7fb3a996"


    def get(self, location):
        url='http://api.openweathermap.org/data/2.5/weather'
        params = {
            'units': 'metric',
            'q': location,
            'appid': self.key,
        }
        data = requests.get(url, params).json()        
        return {
                'date': datetime.fromtimestamp( data["dt"]).strftime('%Y-%m-%d %H:%M:%S'),
                'mint': data["main"]["temp_min"],
                'maxt': data["main"]["temp_max"],
                'location': location,
                'humidity': data["main"]["humidity"],
                'feels_like': data["main"]["feels_like"]
            }
            
        



class DataUpdater(Thread):
    def __init__(self, db, updateTime, location='Volgograd,Russia'):
        Thread.__init__(self,daemon=True)
        self.db = db
        self.time = updateTime
        self.location=location
        self.isUpdated=False

    
    def run(self):
        provider = OpenWeatherProvider()
        while True:           
            data=provider.get(self.location)
            
            if self.db.checkDateInBase(data["date"], data["location"]):
                self.db.insert('weather',data)
                self.isUpdated=True
            time.sleep(self.time)
    