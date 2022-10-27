import random

area = [[0,0,0,0,0], [-1,0,0,0,0], [0,0,0,0,0], [0,1,0,0,0], [0,0,0,0,0]]
cur_pos = [0,0]

def get_max(pos, explore=True):
    
    values = {}
    
    if pos[0]-1 > -1:

        v = area[pos[0]-1][pos[1]]
        values[pos[0]-1, pos[1]] = v

    if pos[0]+1 < 5:

        v = area[pos[0]+1][pos[1]]
        values[pos[0]+1, pos[1]] = v

    if pos[1]-1 > -1:
        v = area[pos[0]][pos[1]-1]
        values[pos[0], pos[1]-1] = v

    if pos[1]+1 < 5: 
        v = area[pos[0]][pos[1]+1]
        values[pos[0], pos[1]+1] = v
    else:
        pass
    
    if explore:
        c = random.choice(list(values.keys()))
        return [c, values[c]]
        
    else:
        max_v = max(values, key = lambda x: values[x])
        return [max_v, values[max_v]]

e = 2
d = 0
g = 0.9
a = 0.1
for i in range(300):
    
    
    for i in range(10):
        r = random.random()
        if r < e:
            explored = True
        else:
            explored = False
        
        c, v = get_max(cur_pos, explore=explored)
        if area[cur_pos[0]][cur_pos[1]] == 1 or area[cur_pos[0]][cur_pos[1]] == -1:
            pass
        else:
            area[cur_pos[0]][cur_pos[1]] = round((1-a)*area[cur_pos[0]][cur_pos[1]] + a*(v*g), 3)         
        cur_pos = c
    e = e * d
    cur_pos = [random.randint(0, len(area)-1), 
           random.randint(0, len(area)-1)]



for i in area:
    print(i)
    print("")
        
        
        
    
    
    


