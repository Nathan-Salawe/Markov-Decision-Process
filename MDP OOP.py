from tkinter import *
from tkinter import ttk
import pandas as pd
import shelve as sv
import random
import time

def get_current():
    nu = 0
    with sv.open('Externals') as ext:
        nu = ext["current"]
    return nu

LARGE_FONT = ('verdana', 12)
small_font = ('verdana', 10)

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
        for F in (StartPage, LayoutPage):
            frame = F(container, self)
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frames(StartPage)

    def show_frames(self, controller):
        frame = self.frames[controller]
        try:
            frame.refresh_()
        except AttributeError:
            pass
        frame.tkraise()
    def update_func(self):
        self.update()
        
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
                                  command=lambda :controller.show_frames(LayoutPage))
        start_button.grid(row=0, column=0, sticky='nsew')
        quit_button = ttk.Button(button_container, text='Quit', command=root.destroy)
        quit_button.grid(row=1, column=0, sticky='nsew')
        
        label_1 = ttk.Label(self, text='')
        label_1.grid(row=0, column=0, rowspan=3, sticky='nsew')
        
        label_1 = ttk.Label(self, text='')
        label_1.grid(row=0, column=2, rowspan=3, sticky='nsew')
        

    def update_selection(self, text):
        with sv.open('Externals') as ext:
            ext["current"] = text
        self.current_selection_label.config(text='Current Selection: ' + str(text))

class LayoutPage(Frame):

    def __init__(self, parent, controller):
        
        Frame.__init__(self, parent)
        
        self.colormap = ['#e0ffd0', '#e6ffd8', '#c3ffa2', '#94ff5a', '#75ff2a', '#59ff00', 
                         '#56f400', '#52e900', '#4ddb00', '#45c400']
        
        self.obstacle_color = 'light grey'
        self.states_color = 'white'
        self.agent_color = 'purple'
        self.destination_color = 'cyan'
        self.controller = controller
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=15)
        self.columnconfigure(0, weight=10)
        
        self.utility_frame = Frame(self)
        self.utility_frame.grid(row=0, column=0, sticky='nsew')
        self.utility_frame.rowconfigure(0, weight=1)
        self.utility_frame.columnconfigure(0, weight=1)
        self.utility_frame.columnconfigure(1, weight=1)
        self.utility_frame.columnconfigure(2, weight=1)
        self.utility_frame.columnconfigure(3, weight=1)
        
        self.layout_frame = Frame(self)
        self.layout_frame.grid(row=1, column=0, sticky='nsew')
        
        bg_c = 'light blue'
        self.back_button = Button(self.utility_frame, text='<---',
                                  command=self.backtrack, borderwidth=0, bg=bg_c, font=LARGE_FONT)
        self.back_button.grid(row=0, column=0, sticky='nsew')
        
        self.refresh_button = Button(self.utility_frame, text='Refresh',
                                     command = self.refresh_, borderwidth=0, bg=bg_c, font=small_font)
        self.refresh_button.grid(row=0, column=3, sticky='nsew')
        
        self.quit_button = Button(self.utility_frame, text='Quit', 
                                  command = self.stop_function, borderwidth=0, bg=bg_c, font=small_font)
        self.quit_button.grid(row=0, column=2, sticky='nsew')
        
        self.go_button = Button(self.utility_frame, text='Go!!', fg='green',
                                command = self.game, borderwidth=0, bg=bg_c, font=small_font)
        self.go_button.grid(row=0, column=1, sticky='nsew')
        
        self.track = []
        
        self.mapkey = {}
        i = 1
        j = 1
        for steps in range(len(self.colormap)):
            self.mapkey[str(i)] = j
            i = round(i - 0.1, 1)
            j += 1
            
    def refresh_(self):
        layout = get_current()
        self.create_layout(layout, self.layout_frame)
        self.obstacles(layout)
        self.agent_pos = [0, 0]
        self.all_states = {}
        self.available_states = {}
        
        for i in range(layout[0]):
            self.update()
            for j in range(layout[1]):        
                curr = []
                avai = []
                if j + 1 < layout[1]:
                    curr.append([i, j+1])
                    if self.lay_grid[i][j+1].cget('bg') == self.states_color:
                        avai.append([i, j+1])
                if i + 1 < layout[0]:
                    curr.append([i+1, j])
                    if self.lay_grid[i+1][j].cget('bg') == self.states_color:
                        avai.append([i+1, j])
                if i - 1 >= 0:
                    curr.append([i-1, j])                    
                    if self.lay_grid[i-1][j].cget('bg') == self.states_color:
                        avai.append([i-1, j])
                if j - 1 >= 0:
                    curr.append([i, j-1])
                    if self.lay_grid[i][j-1].cget('bg') == self.states_color:
                        avai.append([i, j-1])
                self.all_states[i, j] = curr
                self.available_states[i, j] = avai
        
        self.present_state = self.lay_grid[self.agent_pos[0]][self.agent_pos[1]]
        self.present_state.configure(bg=self.agent_color)
        self.destination = self.lay_grid[layout[0] - 1][layout[1] - 1]
        self.destination.configure(bg=self.destination_color)
        self.destination.configure(borderwidth=5, relief='groove')
        
    def create_layout(self, size, frame):
        self.lay_grid = []
        for row in range(size[0]):
            self.update()
            frame.rowconfigure(row, weight=1)
        for col in range(size[1]):
            self.update()
            frame.columnconfigure(col, weight=1)
        
        for r in range(size[0]):
            self.update()
            grid_row = []
            for c in range(size[1]):
                self.update()
                button = Button(frame, text= ' ', bg=self.states_color, borderwidth=0)
                button.grid(row=r, column=c, sticky='nsew')
                grid_row.append(button)
                self.update()
            self.lay_grid.append(grid_row)

    def change_state(self, current_state):
        # function for a random search Algorithm that will precede the MDP algorithm
        p = 0
        n = 0
        if self.lay_grid[current_state[0]][current_state[1]].cget('text') == ' ':
            self.lay_grid[current_state[0]][current_state[1]].configure(text=1)
            color = self.colormap[0]
            self.lay_grid[current_state[0]][current_state[1]].configure(bg=color, fg=color)
            self.update()
            p = 1
            n = 1
        else:
            prior = self.lay_grid[current_state[0]][current_state[1]].cget('text')
            txt = round(prior - 0.1, 1)
            self.lay_grid[current_state[0]][current_state[1]].configure(text=txt)
            key = self.mapkey[str(txt)]
            color = self.colormap[key]
            self.lay_grid[current_state[0]][current_state[1]].configure(bg=color, fg=color)
            self.update()
            p = txt

        next_states = self.available_states[tuple(current_state)]
        states_val = []
        free_states = []
        
        for i in next_states:
            self.update()
            if self.lay_grid[i[0]][i[1]].cget('text') == ' ':
                free_states.append(i)
            else:
                states_val.append([i, self.lay_grid[i[0]][i[1]].cget('text')])
                
        self.update()
        
        if len(free_states) > 0:    
            return [random.choice(free_states), [p, n]]
        else:
            curr = states_val[0]
            multi = []
            for i in states_val:
                if i[1] > curr[1]:
                    curr = i
                    multi = []
                    multi.append(i)
                elif i[1] == curr[1]:
                    multi.append(i)
            return [random.choice(multi)[0], [p, n]]
        
    def MDP_algorithm(self):
        pass

    def obstacles(self, size):
        # create random obstacles on the layout
        # Needs more work lol
        difficulty = 0.3
        no_row_obs = round(size[0] * difficulty)
        no_col_obs = round(size[1] * difficulty)

        chosen_row = random.choices([i for i in range(size[0])], k=no_row_obs)
        
        for i in chosen_row:
            to_edit = random.choices([i for i in range(size[1])], k=no_col_obs)
            for j in to_edit:
                self.lay_grid[i][j].configure(bg=self.obstacle_color)
                self.update()

    def backtrack(self):
        self.layout_frame.destroy()
        self.controller.show_frames(StartPage)
        
    def stop_function(self):
        # remember to save th policy after implimenting the mdp
        root.destroy()
    
    def game(self):
        points = 0
        n = 0
        avg_points = 1
        avg_unique = 1
        
        i = 1
        # while avg_points > 0.92 and avg_unique > 0.5:
        for bb in range(1000):
            stat = self.change_state(self.agent_pos)
            next_state = stat[0]
            points += stat[1][0]
            n += stat[1][1]
            self.lay_grid[next_state[0]][next_state[1]].configure(bg=self.agent_color)
            self.agent_pos = next_state
            self.update()
            self.after(10)
            self.update()
            avg_points = points/i
            avg_unique = n/i           
            i += 1
        


app = MDP()
root.mainloop()

























