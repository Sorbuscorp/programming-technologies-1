from Database import Database as db
from Updater import DataUpdater
from GUI import GuiThread
import time
import sys


class ThreadsHandler():
    def __init__(self,db, locations ,time):
        self.updateTime=time
        self.threads=[DataUpdater(db, time, location) for location in locations]
        self.threads.append(GuiThread(db, locations))
        self.startThreads()#map(lambda t: t.start(), self.threads) #запуск всех потоков
        
        pass

    def startThreads(self):
        for i in self.threads:
            i.start()    

    def GuiIsActive(self):
        return self.threads[-1].is_alive()

    def run(self):
        while self.GuiIsActive():
            self.dataIsUpdate()
            time.sleep(1)
        quit()



    def dataIsUpdate(self):
        isUpdate=False
        for i in self.threads[:-1]:
            isUpdate= i.isUpdated or isUpdate
            if i.isUpdated:
                i.isUpdated=False
                
        if not self.GuiIsActive():
            quit()

        if isUpdate:
            self.threads[-1].app.update()
    

database = db('sqlite:///weather.sqlite3')
database.addTable('weather', date='string', mint='float', maxt='float', location='string', humidity='float',feels_like="float")
database.createBase()

locations = ["Moscow","Volgograd","New York"]

try:
    ThreadsHandler(database, locations, 30).run()
except SystemExit:
    quit()


    


