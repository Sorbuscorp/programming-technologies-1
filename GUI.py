import tkinter as tk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from threading import Thread
from matplotlib.figure import Figure
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from tkinter import messagebox
from datetime import datetime

DATA_UPDATED_EVENT = "<<DataUpdated>>"

class Window(tk.Frame):
    def __init__(self, db, locationsList=None, master=None):
        self.root=master
        self.locations=locationsList
        self.db=db
        self.df={}
        tk.Frame.__init__(self,master)
        self.createWidgets()
        self.root.resizable(False, False)      
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing) 
        self.isCreated=True

    def getData(self):
        for location in self.locations:
            data=self.db.selectWeatherByLocation(location)
            data=[t for t in data]
            self.df[location]={
                "tmin":[t["mint"] for t in data],
                "tmax":[t["maxt"] for t in data],
                "tfeel":[t["feels_like"] for t in data],
                "hum":[t["humidity"] for t in data],
                "dates":[t["date"] for t in data]
            }
   
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
           



    def drawTemperature(self, row, location):
        dates=self.df[location]["dates"]
        tk.Label(text=location).grid(row=row,column=0)
        fig=Figure(figsize=(8,3),constrained_layout=True)
        axes1=fig.add_subplot(111)
        axes1.plot(dates, self.df[location]["tmin"], color = 'blue', label='Min temp')
        axes1.plot(dates, self.df[location]["tmax"], color = 'red', label='Max temp')
        axes1.plot(dates, self.df[location]["tfeel"], color = 'black', label='Feel like temp')

        axes1.legend()

        plt.setp(axes1.get_xticklabels(), fontsize=7)
        plt.setp(axes1.get_xticklabels(), rotation=30)
        FigureCanvasTkAgg(fig,master=self.root).get_tk_widget().grid(row=row+1,column=0)
        

    def drawHumidity(self, row, location):
        fig2=Figure(figsize=(8, 3),constrained_layout=True)
        axes2=fig2.add_subplot(111)
        axes2.plot(self.df[location]["dates"], self.df[location]["hum"])
        FigureCanvasTkAgg(fig2,master=self.root).get_tk_widget().grid(row=row+1,column=1)

        axes2.set(ylim=(0,100))
        plt.setp(axes2.get_xticklabels(), fontsize=7)
        plt.setp(axes2.get_xticklabels(), rotation=30)


    def createWidgets(self):
        print("update gui")
        self.getData()
        row=0
        for k in self.df:
            self.drawTemperature(row,k)
            self.drawHumidity(row,k)
            row=row+2

    def update(self):
        self.createWidgets()




class GuiThread(Thread):
    def __init__(self, db, locationsList):
        Thread.__init__(self)
        self.db = db
        self.locations=locationsList
        self.isUpdate=False
        self.app = None
       
    # def update(self):
    #     print("update gui")
    
    def run(self):
        root=tk.Tk()
        self.app=Window(self.db, self.locations, master=root)
        root.mainloop()
        return
        