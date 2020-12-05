import tkinter as tk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from datetime import datetime

class Window(tk.Frame):
    def __init__(self, db, locationsList=None, master=None):
        self.root=master
        self.locations=locationsList
        self.db=db
        self.df={}
        tk.Frame.__init__(self,master)
        self.createWidgets()

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

    def createWidgets(self):
        self.getData()
        row=0
        for k in self.df:
            dates=self.df[k]["dates"]
            tk.Label(text=k).grid(row=row,column=0)
            fig=Figure(figsize=(8,2))
            axes1=fig.add_subplot(111)
            axes1.plot(dates, self.df[k]["tmin"], color = 'blue')
            axes1.plot(dates, self.df[k]["tmax"], color = 'red')
            axes1.plot(dates, self.df[k]["tfeel"], color = 'black')
            #plt.setp(axes1.get_xticklabels(), rotation=90)

            fig2=Figure(figsize=(8, 2))
            axes2=fig2.add_subplot(111)
            axes2.plot(self.df[k]["dates"], self.df[k]["hum"])

            FigureCanvasTkAgg(fig,master=self.root).get_tk_widget().grid(row=row+1,column=0)
            FigureCanvasTkAgg(fig2,master=self.root).get_tk_widget().grid(row=row+1,column=1)
            row=row+2

            


        # fig=Figure(figsize=(5, 4))
        # fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
        # canvas=FigureCanvasTkAgg(fig,master=self.root)
        # canvas.get_tk_widget().grid(row=0,column=1)
        # canvas.show()

        # self.plotbutton=tk.Button(master=self.root, text="plot", command=lambda: self.plot(canvas,ax))
        # self.plotbutton.grid(row=0,column=0)

    def plot(self,canvas,ax):
        while True: #infinite loop, reads data of a subprocess
            theta=1
            r=2
            ax.plot(theta,r,linestyle="None",maker='o')
            canvas.draw()
            ax.clear()
            #here set axes
        






# root = tkinter.Tk()
# root.wm_title("Weather")

# fig = Figure(figsize=(5, 4), dpi=100)
# t = np.arange(0, 3, .01)
# fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

# canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
# canvas.draw()
# canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

# toolbar = NavigationToolbar2Tk(canvas, root)
# toolbar.update()
# canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


# def on_key_press(event):
#     print("you pressed {}".format(event.key))
#     key_press_handler(event, canvas, toolbar)


# canvas.mpl_connect("key_press_event", on_key_press)


# def _quit():
#     root.quit()     # stops mainloop
#     root.destroy()  # this is necessary on Windows to prevent
#                     # Fatal Python Error: PyEval_RestoreThread: NULL tstate


# button = tkinter.Button(master=root, text="Quit", command=_quit)
# button.pack(side=tkinter.BOTTOM)

# tkinter.mainloop()
