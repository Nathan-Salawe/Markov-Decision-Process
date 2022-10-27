from tkinter import Frame, Button, Label
import random

from . import app
from . import startpage

LARGE_FONT = ('verdana', 12)
small_font = ('verdana', 10)


class LayoutPage(Frame):

    def __init__(self, parent, controller):
        
        Frame.__init__(self, parent)
        
        self.obstacle_color = 'light grey'
        self.states_color = 'white'
        self.agent_color = 'purple'
        self.destination_color = 'cyan'
        self.controller = controller
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=15)
        self.columnconfigure(0, weight=10)
        self.policy = False
        
        self.utility_frame = Frame(self)
        self.utility_frame.grid(row=0, column=0, sticky='nsew')
        self.utility_frame.rowconfigure(0, weight=1)
        self.utility_frame.columnconfigure(0, weight=3)
        self.utility_frame.columnconfigure(1, weight=3)
        self.utility_frame.columnconfigure(2, weight=3)
        self.utility_frame.columnconfigure(3, weight=3)
        self.utility_frame.columnconfigure(4, weight=1)
                
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
                                command = lambda: self.game(self.agent_pos), borderwidth=0, bg=bg_c, font=small_font)
        self.go_button.grid(row=0, column=1, sticky='nsew')
        
        self.status = Label(self.utility_frame, text=0, fg='green', 
                            borderwidth=0, bg=bg_c, font=small_font)
        self.status.grid(row=0, column=4, sticky='nsew')
        
            
    def refresh_(self):
        self.layout = app.get_current()
        self.create_layout(self.layout, self.layout_frame)
        self.obstacles(self.layout)
        self.agent_pos = [0, 0]
        self.all_states = {}
        self.available_states = {}
        
        for i in range(self.layout[0]):
            self.update()
            for j in range(self.layout[1]):        
                curr = []
                avai = []
                if j + 1 < self.layout[1]:
                    curr.append([i, j+1])
                    if self.lay_grid[i][j+1].cget('bg') == self.states_color:
                        avai.append([i, j+1])
                if i + 1 < self.layout[0]:
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
        self.destination_coor = [self.layout[0] - 1, self.layout[1] - 1]
        self.destination = self.lay_grid[self.destination_coor[0]][self.destination_coor[1]]
        self.destination.configure(bg=self.destination_color, text=1)
        self.destination.configure(borderwidth=5, relief='groove')
        
    def create_layout(self, size, frame):
        
        self.lay_grid = []
        for row in range(size[0]):
            self.update()
            frame.rowconfigure(row, weight=1)
            grid_row = []
            for col in range(size[1]):
                self.update()
                frame.columnconfigure(col, weight=1)

                self.update()
                button = Button(frame, text= 0, bg=self.states_color, borderwidth=0, 
                                command = lambda x = [row, col]: self.game(x))
                button.grid(row=row, column=col, sticky='nsew')
                grid_row.append(button)
                self.update()
            self.lay_grid.append(grid_row)


    def get_max(self, pos, limit, explore=True):
        
        values = {}
        
        if pos[0]-1 > -1:
    
            v = self.lay_grid[pos[0]-1][pos[1]].cget('text')
            values[pos[0]-1, pos[1]] = v
    
        if pos[0]+1 < limit[0]:
    
            v = self.lay_grid[pos[0]+1][pos[1]].cget('text')
            values[pos[0]+1, pos[1]] = v
    
        if pos[1]-1 > -1:
            v = self.lay_grid[pos[0]][pos[1]-1].cget('text')
            values[pos[0], pos[1]-1] = v
    
        if pos[1]+1 < limit[1]: 
            v = self.lay_grid[pos[0]][pos[1]+1].cget('text')
            values[pos[0], pos[1]+1] = v
        
        if explore:
            c = random.choice(list(values.keys()))
            return [c, values[c]]
            
        else:
            max_v = max(values, key = lambda x: values[x])
            return [list(max_v), values[max_v]]

        
    def mdp_algorithm(self):
        
        e = 1
        d = 0.8
        g = 0.9
        a = 0.9
        
        episode = (self.layout[0] * self.layout[1]) * 12
        epoch = self.layout[0] * self.layout[1]
        turns = 0
        cur_pos = self.agent_pos
        
        for _ in range(episode):
            turns += 1
            
            if turns == 100:
                overall = self.status.cget('text')
                self.status.configure(text=turns + overall)
                turns = 0
            
            self.update()
            for _ in range(epoch):
                self.update()
                r = random.random()
                if r < e:
                    explored = True
                else:
                    explored = False
                
                c, v = self.get_max(cur_pos, self.layout, explore=explored)
                if self.lay_grid[cur_pos[0]][cur_pos[1]].cget('text') == 1 or self.lay_grid[cur_pos[0]][cur_pos[1]].cget('text') == -1:
                    break
                else:
                    v_s = round((1-a)*self.lay_grid[cur_pos[0]][cur_pos[1]].cget('text') + a*(v*g), 3)
                    self.lay_grid[cur_pos[0]][cur_pos[1]].configure(text= v_s)          
                cur_pos = c
            e = e * d
            cur_pos = [random.randint(0, self.layout[0]-1), 
                       random.randint(0, self.layout[1]-1)]
            self.policy = True

            
    def obstacles(self, size):
        # create random obstacles on the layout
        # Needs more work lol

        difficulty = 0.3 
        matrix_dimension = size[0] * size[1]
        no_of_obstacles = matrix_dimension * difficulty

        for _ in range(round(no_of_obstacles)):
            x = random.randint(0, (size[0] -1))
            y = random.randint(0, (size[1] -1))

            self.lay_grid[x][y].configure(bg=self.obstacle_color)
            self.lay_grid[x][y].configure(text=-1)
            self.update()

    def backtrack(self):
        # self.layout_frame.destroy()
        self.controller.show_frames(startpage.StartPage)
        
    def stop_function(self):
        # remember to save th policy after implimenting the mdp
        app.root.destroy()
    
    def game(self, pos):
        
            if self.policy == False:
                self.mdp_algorithm()
            
            self.destination.configure(bg=self.destination_color)
            trail = []
            self.agent_pos = pos
            while True:

                next_state, v = self.get_max(self.agent_pos, self.layout, explore=False)
                
                self.lay_grid[self.agent_pos[0]][self.agent_pos[1]].configure(bg=self.agent_color)
                trail.append(self.agent_pos)
                
                try:
                    prev = trail[-2]
                    self.lay_grid[prev[0]][prev[1]].configure(bg=self.states_color)
                except IndexError:
                    pass
                
                if self.agent_pos == self.destination_coor:
                    break
        
                self.agent_pos = next_state
                self.update()
                self.after(100)
                self.update()
