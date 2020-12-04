import requests
from Database import Database as db


class WeatherProvider:
    def __init__(self, key):
        self.key = key

    def get(self, location, start_date, end_date):
        url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/history'
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



database = db('sqlite:///weather.sqlite3')
database.addTable('weather', date='string', mint='float', maxt='float', location='string', humidity='float')
database.createBase()

provider = WeatherProvider('373QC5VVYP15RYE4BWGAIXRXY')
data=provider.get('Volgograd,Russia', '2020-09-20', '2020-09-29')
if not database.insert('weather',data):
    print("Error") 
    exit(1)

for row in database.select('weather'):
    print(row)
