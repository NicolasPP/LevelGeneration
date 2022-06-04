import pygame
from config import *
from random import randint, randrange
from cell_state import State

pygame.init()
class Cell:
    islands = []
    cell_neighbour_20 = {}
    cell_neighbour_8 = {}
    cell_neighbour_4 = {}
    cell_grid = []
    row_num = 0
    column_num = 0
    
    ## info ##
    cell_size = 20 
    points = []
    
    
    def __init__(self, screen, left, top, is_edge, r, c):
        Cell.screen = screen
        self.r = r
        self.c = c
        self.cell_size = Cell.cell_size
        self.is_edge = is_edge
        self.left = left
        self.top = top
        self.rect = pygame.Rect(left, top, Cell.cell_size, Cell.cell_size)
        self._state = State.dead.value if is_edge else randint(State.dead.value, State.alive.value)
        self.territory = None
        self.alpha_surface = pygame.Surface(self.rect.size)

    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, new_state):
        self._state = new_state
        self.draw()

    @state.deleter
    def state(self):
        del self._state 

    def draw_alpha(self, colour, alpha):
        self.alpha_surface.set_alpha(alpha)
        self.alpha_surface.fill(colour)
        Cell.screen.surface.blit(self.alpha_surface, self.rect)

    def draw(self, colour = False):
        if not colour:
            colour = self.get_colour()
        pygame.draw.rect(Cell.screen.surface, colour, self.rect)

    def is_clicked(self):
        return pygame.Rect.collidepoint(self.rect,pygame.mouse.get_pos())
    
    def get_colour(self):
        if self.state == State.dead.value : return DEAD
        if self.state == State.alive.value : return ALIVE
        if self.state == State.rock.value : return ROCK
        if self.state == State.lake.value : return LAKE
        if self.state == State.path.value : return PATH

    def get_distance(self, cell):
        return abs(abs(self.r - cell.r) + abs(self.c - cell.c))
    @staticmethod
    def draw_all():
        Cell.screen.surface.fill('Blue')  
        for r in range(Cell.row_num):
            for c in range(Cell.column_num):
                Cell.cell_grid[r][c].draw()
    @staticmethod
    def set_all_surface_alpha(alpha):
        for r in range(Cell.row_num):
            for c in range(Cell.column_num):
                Cell.cell_grid[r][c].alpha_surface.set_alpha(alpha)
    @staticmethod
    def reset_info():
        Cell.points = []    

# Draw functions
def colour_cells(cells, colour):
    for cell in cells:
        cell.draw(colour)
def display_key_binds(show_key_binds, screen):
    if show_key_binds:
        pos_x = (screen.current_width // 2) - 100
        pos_y = 30
        for key, purpose in KEY_BINDS.items():
            info = f'{key} : {purpose}'
            display_info(info, pos_x, pos_y)
            pos_y += 20
def display_info(info, x = 10, y = 10):    
    font = pygame.font.Font(None, 20)
    debug_render = font.render(info,True,'White')
    debug_rect = debug_render.get_rect(topleft = (x,y))
    pygame.draw.rect(pygame.display.get_surface(), 'Black', debug_rect)
    pygame.display.get_surface().blit(debug_render, debug_rect)
def display_territories(screen, show_territories):
    if show_territories:
        for r in range(Cell.row_num):
            for c in range(Cell.column_num):
                cell = Cell.cell_grid[r][c]
                if cell.territory:
                    cell.draw_alpha(cell.territory, 5)
    else:
         Cell.set_all_surface_alpha(0)

# Helper functions
def get_neighbours20(r, c):
    row = Cell.row_num - 1
    column = Cell.column_num -1
    neighbours = get_neighbours8(r, c)

    # top
    pos_x = c - 1
    pos_y = r - 2
    if pos_y >= 0:
        for i in range(3):
            if pos_x + i >= 0 and pos_x + i <= column:
                neighbours.append(Cell.cell_grid[pos_y][pos_x + i])
    # bottom
    pos_x = c + 1
    pos_y = r + 2
    if pos_y <= row:
        for i in range(3):
            if pos_x - i>= 0 and pos_x- i<= column:
                neighbours.append(Cell.cell_grid[pos_y][pos_x - i])
    #left
    pos_x = c - 2
    pos_y = r - 1
    if pos_x >= 0:
        for i in range(3):
            if pos_y + i >= 0 and pos_y + i <= row:
                neighbours.append(Cell.cell_grid[pos_y + i][pos_x])
    #right
    pos_x = c + 2
    pos_y = r + 1
    if pos_x <= column:
        for i in range(3):
            if pos_y - i >= 0 and pos_y - i <= row:
                neighbours.append(Cell.cell_grid[pos_y - i][pos_x])
    
    return neighbours
def get_neighbours8(r,c):
    row = Cell.row_num - 1
    column = Cell.column_num - 1
    neighbours = get_neighbours4(r, c)
    if r + 1 <= row and c -1 >= 0:
        neighbours.append(Cell.cell_grid[r+1][c-1])
    if r + 1 <= row and c + 1 <= column:
        neighbours.append(Cell.cell_grid[r+1][c+1])
    if r - 1 >= 0 and c + 1 <= column:
        neighbours.append(Cell.cell_grid[r-1][c+1])
    if r - 1 >= 0 and c - 1 >= 0:
        neighbours.append(Cell.cell_grid[r-1][c-1])
        
    return neighbours
def get_neighbours4(r,c):
    row = Cell.row_num - 1
    column = Cell.column_num - 1
    neighbours = []
    if r + 1 <= row:
        neighbours.append(Cell.cell_grid[r + 1][c])
    if r - 1 >= 0:
        neighbours.append(Cell.cell_grid[r-1][c])
    if c + 1 <= column:
        neighbours.append(Cell.cell_grid[r][c + 1])
    if c - 1 >= 0:
        neighbours.append(Cell.cell_grid[r][c - 1]) 
    return neighbours
def generate_cells(screen):
    columns = screen.current_width // Cell.cell_size
    rows = screen.current_height // Cell.cell_size
    Cell.column_num = columns
    Cell.row_num = rows
    cell_grid = [[Cell(screen, c * Cell.cell_size,r * Cell.cell_size, is_edge(r, c), r, c) 
                  for c in range(columns)]
                 for r in range(rows)]
    Cell.cell_grid = cell_grid
    Cell.cell_neighbour_8 = get_neighbour_dict(get_neighbours8)
    Cell.cell_neighbour_4 = get_neighbour_dict(get_neighbours4)
    Cell.cell_neighbour_20 = get_neighbour_dict(get_neighbours20)
    Cell.draw_all()
def set_state(cells, state):
    for cell in cells:
        cell.state = state
def flip_state(cells):
    # any state other than alive will set the state to alive 
    for cell in cells:
        cell.state = State.dead.value if cell.state == State.alive.value else State.alive.value
def get_neighbour_dict(neighbour_func):
    #max 8 neigbours
    result = {}
    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            result[
                Cell.cell_grid[r][c]
            ] = neighbour_func(r, c)
    return result
def is_edge(r, c):
    return r == 0 or c == 0 or r == Cell.row_num - 1 or c == Cell.column_num -1
# handle user input
def handle_cell_size_increase(change, screen):
    new_size = Cell.cell_size + change
    if new_size <= screen.current_height // 10 and new_size <= screen.current_width // 10:
        Cell.cell_size = new_size
    generate_cells(screen)
def handle_cell_size_decrease(change, screen):
    new_size = Cell.cell_size - change
    if new_size > 0:
        Cell.cell_size = new_size
    generate_cells(screen)      
def handle_cell_size_change(new_size, screen):
     if new_size >= 5 and new_size <= screen.current_width // 10 and new_size <= screen.current_height:
            Cell.cell_size = new_size   
def handle_cell_mouse_click(screen):
    pos = pygame.mouse.get_pos()
    cart_pos = screen_to_cartesian(pos[0], pos[1], screen.current_height, screen.current_width)
    Cell.points.append(pos)
    pygame.draw.circle(screen.surface, 'white', pos, 3, 2)
    

## temp functions
def get_edge_start_end(pair, screen, slope, mid_point):
    line_list = get_line_list(screen, slope, mid_point)
    valid_points = []
    smallest_x = (screen.current_width // 2) + 1
    largest_x = (- screen.current_width // 2) - 1
    for plot in line_list:
        pair_dist = distance_squared(pair[0], plot)
        for point in Cell.points:
            if point not in pair:
                point_dist = distance_squared(point, plot)
                if pair_dist <= point_dist:
                    if plot[0] <= smallest_x: smallest_x = plot[0]
                    if plot[0] >= largest_x: largest_x = plot[0]
                    valid_points.append(plot)
    start = smallest_x, get_y(smallest_x, slope, mid_point)
    end = largest_x, get_y(largest_x, slope, mid_point)
    return start, end

def get_line(pair, screen, slope, mid_point):
    smallest_x = - screen.current_width // 2
    largest_x = screen.current_width // 2
    s_dist= distance_squared((smallest_x, 0), mid_point)
    l_dist = distance_squared((largest_x, 0), mid_point)
    new_x = 0
    small = False
    r = range(-screen.current_width // 2 , (screen.current_width // 2) + 1)
    if s_dist < l_dist:
        r = range(-screen.current_width // 2 , (screen.current_width // 2) + 1)
        small = True
    else:
        r = range(screen.current_width // 2 , (-screen.current_width//2) - 1)
    done = False
    for x in r:
       y = get_y(x, slope, mid_point)
       pair_dist = distance_squared(pair[0], (x, y))
       for point in Cell.points:
           if point not in pair:
               point_dist = distance_squared(point, (x, y))
               if pair_dist >= point_dist:
                   done = True
                   new_x = x
                   break
       if done:
           break        

    pygame.draw.circle(screen.surface, 'orange', (new_x , get_y(new_x, slope, mid_point)), 3 , 2 )
    end = cartesian_to_screen(new_x, get_y(new_x, slope, mid_point), screen.current_height, screen.current_width)
    if small:
        start = cartesian_to_screen(smallest_x, get_y(smallest_x, slope, mid_point), screen.current_height, screen.current_width)
    else:
        start = cartesian_to_screen(largest_x, get_y(largest_x, slope, mid_point), screen.current_height, screen.current_width)
    return start, end

def get_line_list(screen, slope, mid_point):
    r = range(-screen.current_width // 2, (screen.current_width // 2) + 1)
    return list(map(lambda x : (x, slope * ( x - mid_point[0]) + mid_point[1]), r))
    
def simple_dist(a, b):
    x_diff = abs(a[0] - b[0])
    y_diff = abs(a[1] - b[1])
    return x_diff + y_diff

def distance_squared(a, b):
    x = a[0] - b[0]
    y = a[1] - b[1]
    return x*x + y*y

def get_random_points(screen, n):
    points = []
    start = - (screen.current_width // 2)
    end = (screen.current_width // 2) + 1
    while len(points) < n:
        p = randrange(start, end), randrange(start, end)
        if p not in points: points.append(p)
    return points

def get_3_not_so_random_points(screen):
    #cartesian coords points
    height = screen.current_height // 2
    width = screen.current_width // 2
    p1 = randrange(-width, 1), randrange(0, height)
    p2 = randrange(0 , width), randrange(0, height)
    p3 = randrange(-width, height),randrange(-height, 1)
    p1 = cartesian_to_screen(p1[0], p1[1], screen.current_height, screen.current_width)
    p2 = cartesian_to_screen(p2[0], p2[1], screen.current_height, screen.current_width)
    p3 = cartesian_to_screen(p3[0], p3[1], screen.current_height, screen.current_width)
    return [p1,p2,p3]

def get_point_pairs(screen, n):
    pairs = []
    Cell.points = get_3_not_so_random_points(screen)
    Cell.points.append(Cell.points[0])
    size = len(Cell.points)
    for i in range(size):
        if i == size - 1:
            break
        pair = Cell.points[i:i+2]
        pairs.append(tuple(pair))
    return pairs

def get_perpendicular_slope(a , b):
    if a[0] - b[0] == 0 : return 1
    if a[1] - b[1] == 0 : return 1
    return -1 * ((a[0] - b[0]) / (a[1] - b[1]) )

def get_mid_point(a, b): # c=x r=y 
    x_diff = abs((a[0] - b[0]) // 2)
    y_diff = abs((a[1] - b[1]) // 2)
    largest_x = max([a[0], b[0]])
    largest_y = max([a[1], b[1]])
    return (largest_x - x_diff, largest_y - y_diff)

def get_x(y, slope, mid_point):
    return 

def get_y(x, slope, mid_point):
    return slope * ( x - mid_point[0]) + mid_point[1]

def screen_to_cartesian(r, c, current_height, current_width):
    x = r - (current_width // 2)
    y =(-1 * c) + (current_height // 2)
    return x, y

def cartesian_to_screen(x, y, current_height, current_width):
    c = x + (current_width // 2)
    r = (current_height // 2) - y
    return c , r  