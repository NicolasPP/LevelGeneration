import pygame
from config import *
from random import randint

class Cell:
    cell_grid = []
    cell_neighbour = {}
    row_num = 0
    column_num = 0
    
    ## info ##
    cell_size = 20  
    iteration_num = 0
    iteration_new_num = 0
    clean_num = 0
    clean_bigger_num = 0
    clean_huge_num = 0
    wall_num = 0
    wall2_num = 0
    wall3_num = 0
    wall4_num = 0
    
    
    def __init__(self, left, top, is_edge):
        self.cell_size = Cell.cell_size
        self.is_edge = is_edge
        self.rect = pygame.Rect(left, top, Cell.cell_size, Cell.cell_size)
        self.state = 0 if is_edge else randint(0,1)
    
    def draw(self, surface, colour = None):
        if not colour:
            colour =  WALL if self.state == 1 else EMPTY
        pygame.draw.rect(surface, colour, self.rect)

    def is_clicked(self):
        return pygame.Rect.collidepoint(self.rect,pygame.mouse.get_pos())
 
# Draw functions
def draw(surface):
    surface.fill('Blue')  
    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            Cell.cell_grid[r][c].draw(surface)
def draw_cells(cells, surface, colour = None):
    if not colour:
        for cell in cells:
            cell.draw(surface)
    else:
        for cell in cells:
            cell.draw(surface, colour)
def display_current_command(screen, func_index):
    func_name = id_func[func_index].__name__
    info = f'[ {func_name} ]'
    pos_x = (screen.current_width // 2) - 100
    pos_y = 10
    display_info(info, pos_x, pos_y)
def display_current_board_information(show_info):
    info = [
        "--- Current Board Info ---",
        f'cell size : {Cell.cell_size}',
        f'total iterations : {Cell.iteration_num}',
        f'total new iterations : {Cell.iteration_new_num}',
        f'total clean ups : {Cell.clean_num}',
        f'total clean bigger : {Cell.clean_bigger_num}',
        f'total clean huge : {Cell.clean_huge_num}',
        f'total wall : {Cell.wall_num}',
        f'total wall2 :{Cell.wall2_num}',
        f'total wall3 : {Cell.wall3_num}'
    ]
    pos_x = pos_y = 10
    if show_info:
        for inf in info:    
            display_info(inf, pos_x, pos_y)
            pos_y += 20
def display_current_instruction_info(instruction, screen, show_info):
    if show_info:
        pos_x = screen.current_width - 200
        pos_y = 10
        ids = instruction[INFO][INST]
        info_name = "--- Current Instruction ---"
        instruction_name = instruction[NAME]
        instruction_info = f'name : {instruction_name}'
        display_info(info_name, pos_x, pos_y)
        pos_y += 20
        display_info(instruction_info, pos_x, pos_y) 
        if len(ids) > 0:
            instructions_num = get_instruction_amount(instruction[INFO][INST])
            for info in instructions_num:
                pos_y += 20
                name = info[0]
                amount = info[1]
                func_info = f'{name} : {amount}'
                display_info(func_info, pos_x, pos_y)
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
            
# Helper functions
def get_instruction_amount(info):
    result = []
    last = info[0]
    result.append([id_func[last].__name__, 1])
    for id in info[1:]:
        if id == last:
            result[-1][1] += 1
        else:
            result.append([id_func[id].__name__, 1])
        last = id
    return result
def get_cells_to_change(func):
    cells_to_change = []
    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            cell = Cell.cell_grid[r][c]
            if func(cell) and not cell.is_edge:
                cells_to_change.append(cell)
    return cells_to_change
def get_neighbours8(r,c):
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
    if r + 1 <= row and c -1 >= 0:
        neighbours.append(Cell.cell_grid[r+1][c-1])
    if r + 1 <= row and c + 1 <= column:
        neighbours.append(Cell.cell_grid[r+1][c+1])
    if r - 1 >= 0 and c + 1 <= column:
        neighbours.append(Cell.cell_grid[r-1][c+1])
    if r - 1 >= 0 and c - 1 >= 0:
        neighbours.append(Cell.cell_grid[r-1][c-1])
        
    return neighbours
def get_neighbours4(r , c):
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
def is_change_required(cell):
    count = len(list(filter(lambda cell : cell.state == 1, 
               Cell.cell_neighbour[cell])))
    
    if count == 0 or count >= 5 : #wall
        return True if cell.state == 0 else False
    
    if count == 3: #empty
        return True if cell.state == 1 else False
    
    return False
def is_trip_required(cell):
    count = len(list(filter(lambda cell : cell.state == 1, 
               Cell.cell_neighbour[cell])))
    
    if count == 0 or count >= 5 : #wall
        return True 
    
    if count == 4: #empty
        return True
    
    return False
def is_edge(r, c):
    if r == 0 or c == 0 or r == Cell.row_num - 1 or c == Cell.column_num -1:
        return True
    return False
def is_clean(cell, n_num):
    count = len(list(filter(lambda cell : cell.state == 1, 
               Cell.cell_neighbour[cell])))
    
    if count <= n_num:
        return False if cell.state == 1 else True

    return True
def is_wall(cell):
    count = len(list(filter(lambda cell : cell.state == 1, 
               Cell.cell_neighbour[cell])))
    
    if count < 7:
        return True if cell.state == 1 else False

def generate_cells(screen):
    columns = screen.current_width // Cell.cell_size
    rows = screen.current_height // Cell.cell_size
    Cell.column_num = columns
    Cell.row_num = rows
    cell_grid = [[Cell(c * Cell.cell_size,r * Cell.cell_size, is_edge(r, c)) 
                  for c in range(columns)]
                 for r in range(rows)]
    Cell.cell_grid = cell_grid
    generate_neighbour_dict()
    draw(screen.surface)
def generate_neighbour_dict():
    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            Cell.cell_neighbour[
                Cell.cell_grid[r][c]
            ] = get_neighbours8(r, c)

def flip_state(cells):
    for cell in cells:
        cell.state = 0 if cell.state == 1 else 1
def reset_info():
    Cell.iteration_num = 0
    Cell.iteration_new_num = 0
    Cell.clean_num = 0
    Cell.clean_bigger_num = 0
    Cell.clean_huge_num = 0
    Cell.wall_num = 0
    Cell.wall2_num = 0
    Cell.wall3_num = 0
    Cell.wall4_num = 0

def handle_cell_size_increase(change, screen):
    new_size = Cell.cell_size + change
    if new_size <= screen.current_height // 10 and new_size <= screen.current_width // 10:
        Cell.cell_size = new_size
def handle_cell_size_decrease(change):
    new_size = Cell.cell_size - change
    if new_size > 0:
        Cell.cell_size = new_size      
def handle_set_cell_size(new_size, screen):
     if new_size >= 5 and new_size <= screen.current_width // 10 and new_size <= screen.current_height:
            Cell.cell_size = new_size   
def handle_mouse_click(surface):
    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            cell = Cell.cell_grid[r][c]
            if cell.is_clicked():
                n = Cell.cell_neighbour[cell]
                break
    
    draw_cells(n, surface, colour = 'Yellow')
def handle_func_next(func_index):
    size = len(func_id)
    next = func_index + 1
    if next <= size:
        return next
    return func_index
def handle_func_prev(func_index):
    prev = func_index - 1
    if prev >= 1:
        return prev
    return func_index
# Instruction commands
'''
when adding a new command you have to add a variable in the cell class,
add the new fucntion id the id_func and func_id, add it to reset_info, add where it gets updated
'''
def add_walls(surface):
    print("add_walls")
    Cell.wall_num =+ 1
    cells_to_wall = []
    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            cell = Cell.cell_grid[r][c]
            if is_wall(cell):
                cells_to_wall.append(cell)
    draw_cells(cells_to_wall, surface, colour = 'Gray')
def add_walls2(surface):
    Cell.wall2_num += 1
    print("add_walls2")
    dead_cells = []
    cells_to_wall = []

    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            cell = Cell.cell_grid[r][c]
            if cell.state == 0:
                dead_cells.append(cell)

    for cell in dead_cells:
        live_cells = list(filter(lambda cell : cell.state == 1, 
        Cell.cell_neighbour[cell]))
        for c in live_cells:
            if c not in cells_to_wall:
                cells_to_wall.append(c)
    draw_cells(cells_to_wall, surface, 'Gray')
def add_walls3(surface):
    Cell.wall3_num += 1
    print("add_walls3")
    dead_cells = []
    cells_to_wall = []

    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            cell = Cell.cell_grid[r][c]
            if cell.state == 0:
                dead_cells.append(cell)

    for cell in dead_cells:
        for c in Cell.cell_neighbour[cell]:
            if c.state == 1:
                cells_to_wall.append(cell)
                break
    draw_cells(cells_to_wall, surface, 'Gray')
def add_walls4(surface):
    Cell.wall3_num += 1
    print("add_walls4")
    dead_cells = []
    cells_to_wall = []

    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            cell = Cell.cell_grid[r][c]
            if cell.state == 0:
                dead_cells.append([cell, r, c])

    for cell_index in dead_cells:
        for cell in get_neighbours4(cell_index[1], cell_index[2]):
            if cell.state == 1:
                cells_to_wall.append(cell)
    draw_cells(cells_to_wall, surface, 'Gray')
def clean_up(surface):
    print("clean_up")
    Cell.clean_num += 1
    cells_to_kill = []
    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            cell = Cell.cell_grid[r][c]
            if not is_clean(cell, 1):
                cells_to_kill.append(cell)

    flip_state(cells_to_kill)
    draw_cells(cells_to_kill, surface)
def clean_up_bigger(surface):
    print("clean_up_bigger")
    Cell.clean_bigger_num += 1
    cells_to_kill = []
    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            cell = Cell.cell_grid[r][c]
            if not is_clean(cell, 3):
                cells_to_kill.append(cell)

    flip_state(cells_to_kill)
    draw_cells(cells_to_kill, surface)
def clean_up_huge(surface):
    print("clean_up_huge")
    Cell.clean_huge_num += 1
    cells_to_kill = []
    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            cell = Cell.cell_grid[r][c]
            if not is_clean(cell, 4):
                cells_to_kill.append(cell)

    flip_state(cells_to_kill)
    draw_cells(cells_to_kill, surface) 
def randomise(surface):
    print("randomise")
    reset_info()
    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            cell = Cell.cell_grid[r][c]
            cell.state = 0 if cell.is_edge else randint(0,1)
    draw(surface)
def iterate(surface):
    print("iterate")
    Cell.iteration_num += 1
    cells_to_change = get_cells_to_change(is_change_required)
    flip_state(cells_to_change)
    draw_cells(cells_to_change, surface)
def iterate_new(surface):
    print("iterate_new")
    Cell.iteration_new_num += 1
    cells_to_change = get_cells_to_change(is_trip_required)
    flip_state(cells_to_change)
    draw_cells(cells_to_change, surface)


func_id = {
    add_walls: 1,
    clean_up: 2,
    clean_up_bigger: 3,
    clean_up_huge: 4,
    randomise: 5,
    iterate: 6,
    iterate_new: 7,
    add_walls2: 8,
    add_walls3: 9,
    add_walls4: 10,
}
id_func = {
    1: add_walls,
    2: clean_up,
    3: clean_up_bigger,
    4: clean_up_huge,
    5: randomise,
    6: iterate,
    7: iterate_new,
    8: add_walls2,
    9: add_walls3,
    10: add_walls4,
}