from tkinter import Frame
from tkinter import ttk
import shelve as sv

from . import layout
from . import app

LARGE_FONT = ('verdana', 12)
small_font = ('verdana', 10)


class StartPage(Frame):

    def __init__(self, parent, controller):
        
        self.sele = controller
        Frame.__init__(self, parent)
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.sl = [0]
        grid_dict = {}
        r = 0
        c = 0
        for i in range(6, 16, 4):
            for j in range(8, 18, 4):   
                grid_dict['B{}x{}'.format(i, j)] = [[i, j], [r, c]]
                c += 1
                if c == 3:
                    c = 0
            r += 1
            if r == 3:
                r = 0

        top_container = Frame(self)
        top_container.grid(row=0, column=1, sticky='nsew')
        top_container.rowconfigure(0, weight=1)
        top_container.rowconfigure(1, weight=1)
        top_container.columnconfigure(0, weight=9)
        
        button_container = Frame(self)
        button_container.grid(row=2, column=1, sticky='nsew')
        button_container.rowconfigure(0, weight=1)
        button_container.rowconfigure(1, weight=1)
        button_container.columnconfigure(0, weight=9)
        
        options_container = Frame(self)
        options_container.grid(row=1, column=1, sticky='nsew')
        options_container.rowconfigure(0, weight=1)
        options_container.rowconfigure(1, weight=1)
        options_container.rowconfigure(2, weight=1)
        options_container.columnconfigure(0, weight=1)
        options_container.columnconfigure(1, weight=1)
        options_container.columnconfigure(2, weight=1)
        
        intro = "Markov Decision Process For Shortest Route Algorithm"
        intro_label = ttk.Label(top_container, text=intro, font=LARGE_FONT)
        intro_label.grid(row=0, column=0, sticky='nsew')
        
        for i in grid_dict:
            button = ttk.Button(options_container, text=str(grid_dict[i][0]), 
                                command = lambda j = grid_dict[i][0]: self.update_selection(j))
            button.grid(row=grid_dict[i][1][0], column=grid_dict[i][1][1], sticky='nsew')
        
        self.current_selection = grid_dict[list(grid_dict.keys())[0]][0]
        
        with sv.open('Externals') as ext:
            ext["current"] = self.current_selection

        self.current_selection_label = ttk.Label(top_container,
                                      text='Current Selection: ' + str(self.current_selection))
        self.current_selection_label.grid(row=1, column=0, sticky='nsew')

        start_button = ttk.Button(button_container, text='Start',
                                  command=lambda :controller.show_frames(layout.LayoutPage))
        start_button.grid(row=0, column=0, sticky='nsew')
        quit_button = ttk.Button(button_container, text='Quit', command=app.root.destroy)
        quit_button.grid(row=1, column=0, sticky='nsew')
        
        label_1 = ttk.Label(self, text='')
        label_1.grid(row=0, column=0, rowspan=3, sticky='nsew')
        
        label_1 = ttk.Label(self, text='')
        label_1.grid(row=0, column=2, rowspan=3, sticky='nsew')
        

    def update_selection(self, text):
        with sv.open('Externals') as ext:
            ext["current"] = text
        self.current_selection_label.config(text='Current Selection: ' + str(text))
