from Database import Database as db
from Updater import DataUpdater
from GUI import Window
import time
import tkinter as tk

database = db('sqlite:///weather.sqlite3')
database.addTable('weather', date='string', mint='float', maxt='float', location='string', humidity='float',feels_like="float")
database.createBase()

locations = ["Moscow","Volgograd","New York"]

for location in locations:
    DataUpdater(database, 20, location).start()


root=tk.Tk()
app=Window(database, locations, master=root)
app.mainloop()


# while True:
#     for location in locations:
#         for row in database.selectWeatherByLocation(location):
#             print(row["location"])
#     time.sleep(10)
