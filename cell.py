import pygame
from config import *
from random import randint

class Cell:
    cell_grid = []
    cell_neighbour = {}
    cell_iteration_num = 0
    row_num = 0
    column_num = 0
    
    def __init__(self, left, top, is_edge, cell_size):
        self.cell_size = cell_size
        self.is_edge = is_edge
        self.rect = pygame.Rect(left, top, cell_size, cell_size)
        self.state = 0 if is_edge else randint(0,1)
    
    def draw(self, surface, colour = None):
        if not colour:
            colour =  WALL if self.state == 1 else EMPTY
        pygame.draw.rect(surface, colour, self.rect)
        
# Draw functions
def draw(surface):
    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            Cell.cell_grid[r][c].draw(surface)
def display_current_board_information(cell_size):
    cell_size_info = f'cell size : {cell_size}'
    
    display_info(cell_size_info)
def display_info(info, y = 10, x = 10):
    font = pygame.font.Font(None, 30)
    debug_render = font.render(info,True,'White')
    debug_rect = debug_render.get_rect(topleft = (x,y))
    pygame.draw.rect(pygame.display.get_surface(), 'Black', debug_rect)
    pygame.display.get_surface().blit(debug_render, debug_rect)

# Helper functions
def get_cells_to_change(func):
    cells_to_change = []
    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            cell = Cell.cell_grid[r][c]
            if func(cell) and not cell.is_edge:
                cells_to_change.append(cell)
    return cells_to_change
def get_neighbours(r,c):
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
        neighbours.append(Cell.cell_grid[r][r - 1])
    if r + 1 <= row and c -1 >= 0:
        neighbours.append(Cell.cell_grid[r+1][c-1])
    if r + 1 <= row and c + 1 <= column:
        neighbours.append(Cell.cell_grid[r+1][c+1])
    if r - 1 >= 0 and c + 1 <= column:
        neighbours.append(Cell.cell_grid[r-1][c+1])
    if r - 1 >= 0 and c - 1 >= 0:
        neighbours.append(Cell.cell_grid[r-1][c-1])
        
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

def generate_cells(screen, cell_size):
    columns = screen.current_width // cell_size
    rows = screen.current_height // cell_size
    Cell.column_num = columns
    Cell.row_num = rows
    cell_grid = [[Cell(c * cell_size,r * cell_size, is_edge(r, c), cell_size) 
                  for c in range(columns)]
                 for r in range(rows)]
    Cell.cell_grid = cell_grid
    generate_neighbour_dict()
def generate_neighbour_dict():
    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            Cell.cell_neighbour[
                Cell.cell_grid[r][c]
            ] = get_neighbours(r, c)

def flip_state(cells):
    for cell in cells:
        cell.state = 0 if cell.state == 1 else 1
# Instruction commands
def add_walls(surface):
    print("add_walls")
    cells_to_wall = []
    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            cell = Cell.cell_grid[r][c]
            if is_wall(cell):
                cells_to_wall.append(cell)
                
    for cell in cells_to_wall:
        cell.draw(surface, 'Gray')
def clean_up(surface):
    print("clean_up")
    cells_to_kill = []
    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            cell = Cell.cell_grid[r][c]
            if not is_clean(cell, 1):
                cells_to_kill.append(cell)

    flip_state(cells_to_kill)
    draw(surface)   
def clean_up_bigger(surface):
    print("clean_up_bigger")
    cells_to_kill = []
    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            cell = Cell.cell_grid[r][c]
            if not is_clean(cell, 3):
                cells_to_kill.append(cell)

    flip_state(cells_to_kill)
    draw(surface)
def clean_up_huge(surface):
    print("clean_up_huge")
    cells_to_kill = []
    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            cell = Cell.cell_grid[r][c]
            if not is_clean(cell, 4):
                cells_to_kill.append(cell)

    flip_state(cells_to_kill)
    draw(surface) 
def randomise(surface):
    print("randomise")
    Cell.cell_iteration_num = 0
    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            cell = Cell.cell_grid[r][c]
            cell.state = 0 if cell.is_edge else randint(0,1)
    draw(surface)
def iterate(surface):
    print("iterate")
    Cell.cell_iteration_num += 1
    cells_to_change = get_cells_to_change(is_change_required)
    flip_state(cells_to_change)
    draw(surface)
def iterate_new(surface):
    print("iterate_new")
    Cell.cell_iteration_num += 1
    cells_to_change = get_cells_to_change(is_trip_required)
    flip_state(cells_to_change)
    draw(surface)
