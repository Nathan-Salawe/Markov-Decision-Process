from tkinter import Frame, Tk
import shelve as sv

from . import startpage
from . import layout

def get_current():
    nu = 0
    with sv.open('Externals') as ext:
        nu = ext["current"]
    return nu

root = Tk()
root.geometry('640x480')

class MDP:

    def __init__(self):
        
        container = Frame(root)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.layout = [6, 8]
        self.frames = {}
        for F in (startpage.StartPage, layout.LayoutPage):
            frame = F(container, self)
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frames(startpage.StartPage)

    def show_frames(self, controller):
        frame = self.frames[controller]
        try:
            frame.refresh_()
        except AttributeError:
            pass
        frame.tkraise()
    def update_func(self):
        self.update()
        