import pygame
import sys as sys
import queue
from collections import deque
from config import *
from random import randint, choice
from cell_state import State
from utils import time_func
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
    iteration_num = 0
    iteration_new_num = 0
    island_round_num = 0
    clean_num = 0
    clean_bigger_num = 0
    clean_huge_num = 0
    wall_num = 0
    wall2_num = 0
    wall3_num = 0
    wall4_num = 0
    
    
    def __init__(self, screen, left, top, is_edge):
        Cell.screen = screen
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

    @staticmethod
    def draw_all():
        Cell.screen.surface.fill('Blue')  
        for r in range(Cell.row_num):
            for c in range(Cell.column_num):
                Cell.cell_grid[r][c].draw()
                

# Draw functions
def colour_cells(cells, colour):
    for cell in cells:
        cell.draw(colour)
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
        f'total wall3 : {Cell.wall3_num}',
        f'total island round {Cell.island_round_num}'
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
def display_territories(screen, show_territories):
    if show_territories:
        for r in range(Cell.row_num):
            for c in range(Cell.column_num):
                cell = Cell.cell_grid[r][c]
                if cell.state == State.alive.value:
                    
                    if cell.left < screen.current_width // 2:
                        cell.draw_alpha('red', 5)
        #                 cell.draw(screen.transparent_surface, 'Pink')
                    else:
                        cell.draw_alpha('pink', 5)
        #                 cell.draw(screen.transparent_surface, 'red')
        # draw_rect_alpha(screen.surface, (0,0,0), (100,100,100,100))
        # screen.surface.blit(screen.transparent_surface, (0, 0))
    else:
         for r in range(Cell.row_num):
            for c in range(Cell.column_num):
                cell = Cell.cell_grid[r][c]
                cell.alpha_surface.set_alpha(0)

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
def get_cells_to_change(func, cell_dict):
    cells_to_change = []
    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            cell = Cell.cell_grid[r][c]
            if func(cell, cell_dict) and not cell.is_edge:
                cells_to_change.append(cell)
    return cells_to_change
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
def get_random_cell_at_edge(island, cell_neighbour):
    valid_cells = get_island_edge_cells(island, cell_neighbour)
    return choice(valid_cells)
def get_island_edge_cells(island, cell_neighbour):
    valid_cells = []
    for cell in island:
        if cell.state != State.rock.value:
            for c in cell_neighbour[cell]:
                if c.state != State.alive.value:
                   valid_cells.append(cell)
                   break
    return valid_cells
def get_island_visited_dict(cell_neighbour):
    # this will consider every state other than dead alive
    result = {}
    for cell in cell_neighbour:
        if cell.state == State.dead.value:
            result[cell] = True
        else:
            result[cell] = False
    return result
def get_lake_visited_dict(cell_neighbour):
    visited = {}
    for cell in cell_neighbour:
        if cell not in visited:
            if cell.state == State.dead.value:
                visited[cell] = False
            else:
                visited[cell] = True
    return visited
def get_neighbour_dict(neighbour_func):
    #max 8 neigbours
    result = {}
    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            result[
                Cell.cell_grid[r][c]
            ] = neighbour_func(r, c)
    return result
def get_longest_path(distance, start):
    dist = 0
    end = start
    path = []
    for cell, path_list in distance.items():
        if len(path_list) > dist:
            dist = len(path_list)
            path = path_list
            end = cell
    return end, path
def get_edge_side(index):
    r = index[0]
    c = index[1]
    left = right = top = bottom = False
    if r == Cell.row_num - 1:top = True
    if r == 0:bottom = True
    if c == Cell.column_num - 1:right = True
    if c == 0:left = True 
    return left, right, top, bottom
def get_islands_extremes(island):
    return left, right, top, bottom

def generate_cells(screen):
    columns = screen.current_width // Cell.cell_size
    rows = screen.current_height // Cell.cell_size
    Cell.column_num = columns
    Cell.row_num = rows
    cell_grid = [[Cell(screen, c * Cell.cell_size,r * Cell.cell_size, is_edge(r, c)) 
                  for c in range(columns)]
                 for r in range(rows)]
    Cell.cell_grid = cell_grid
    Cell.cell_neighbour_8 = get_neighbour_dict(get_neighbours8)
    Cell.cell_neighbour_4 = get_neighbour_dict(get_neighbours4)
    Cell.cell_neighbour_20 = get_neighbour_dict(get_neighbours20)
    Cell.draw_all()
def generate_path_dicts(island):
    visited = {}
    distance = {}
    for cell in island:
        visited[cell] = False
        distance[cell] = []
    return visited, distance

def set_state(cells, state):
    for cell in cells:
        cell.state = state
def flip_state(cells):
    # any state other than alive will set the state to alive 
    for cell in cells:
        cell.state = State.dead.value if cell.state == State.alive.value else State.alive.value
def reset_info():
    Cell.iteration_num = 0
    Cell.iteration_new_num = 0
    Cell.island_round_num = 0
    Cell.clean_num = 0
    Cell.clean_bigger_num = 0
    Cell.clean_huge_num = 0
    Cell.wall_num = 0
    Cell.wall2_num = 0
    Cell.wall3_num = 0
    Cell.wall4_num = 0

# algorithms
def cc_while_dfs(cell, visited, cell_neighbour):
    stack = deque()
    stack.append(cell)
    island = [cell]
    while len(stack):
        c = stack.pop()
        if not visited[c]:
            visited[c] = True
        for n in cell_neighbour[c]:
            if not visited[n]:
                stack.append(n)
                island.append(n)
    return list(set(island))
def all_distances_from_cell(cell, island, cell_neighbour):
    visited, distance = generate_path_dicts(island)
    q = queue.Queue()
    q.put(cell)
    visited[cell] = True
    distance[cell].append(cell)
    count = 0
    while not q.empty():
        a = q.get()
        for c in cell_neighbour[a]:
            if c.state == State.alive.value and not visited[c]:
                distance[c] = distance[a] + [c]
                visited[c] = True
                q.put(c)
    return distance
# board rules
def is_change_required(cell, cell_dict):
    count = len(list(filter(lambda cell : cell.state == State.alive.value, 
               cell_dict[cell])))
    
    if count == 0 or count >= 5 : #wall
        return True if cell.state == State.dead.value else False
    
    if count == 3: #empty
        return True if cell.state == State.alive.value else False
    
    return False
def is_change_big(cell, cell_dict):
    count = len(list(filter(lambda cell : cell.state == State.alive.value, 
               cell_dict[cell])))
    
    if count == 0 or count >= 12 : #wall
        return True if cell.state == State.dead.value else False
    
    if count == 7 : #empty
        return True if cell.state == State.alive.value else False
    
    return False
def is_trip_required(cell, cell_dict):
    count = len(list(filter(lambda cell : cell.state == State.alive.value, 
               cell_dict[cell])))
    
    if count == 0 or count >= 5 : #wall
        return True 
    
    if count == 4: #empty
        return True
    
    return False
def is_edge(r, c):
    if r == 0 or c == 0 or r == Cell.row_num - 1 or c == Cell.column_num -1:
        return True
    return False
def is_clean(cell, n_num, cell_dict):
    count = len(list(filter(lambda cell : cell.state == State.alive.value, 
               cell_dict[cell])))
    
    if count <= n_num:
        return False if cell.state == State.alive.value else True

    return True
def is_wall(cell, cell_dict):
    count = len(list(filter(lambda cell : cell.state == State.alive.value, 
               cell_dict[cell])))
    
    if count < 7:
        return True if cell.state == State.alive.value else False

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
def handle_set_cell_size(new_size, screen):
     if new_size >= 5 and new_size <= screen.current_width // 10 and new_size <= screen.current_height:
            Cell.cell_size = new_size   
def handle_mouse_click(surface):
    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            cell = Cell.cell_grid[r][c]
            if cell.is_clicked():
                n = Cell.cell_neighbour_20[cell]
                break
    
    # colour_cells(n, surface, 'Yellow')


#   Instruction commands
'''
when adding a new command you have to add a variable in the cell class,
add the new fucntion id the id_func and func_id, add it to reset_info, add where it gets updated
'''
@time_func
def add_walls(screen):
    Cell.wall_num =+ 1
    cells_to_wall = []
    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            cell = Cell.cell_grid[r][c]
            if is_wall(cell, Cell.cell_neighbour_8):
                cells_to_wall.append(cell)
    set_state(cells_to_wall, State.rock.value)
@time_func
def add_walls2(screen):
    Cell.wall2_num += 1
    dead_cells = []
    cells_to_wall = []

    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            cell = Cell.cell_grid[r][c]
            if cell.state == State.dead.value:
                dead_cells.append(cell)

    for cell in dead_cells:
        live_cells = list(filter(lambda cell : cell.state == State.alive.value, 
        Cell.cell_neighbour_8[cell]))
        for c in live_cells:
            if c not in cells_to_wall:
                cells_to_wall.append(c)
    set_state(cells_to_wall, State.rock.value)
@time_func
def add_walls3(screen):
    Cell.wall3_num += 1
    dead_cells = []
    cells_to_wall = []

    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            cell = Cell.cell_grid[r][c]
            if cell.state == State.dead.value:
                dead_cells.append([cell, (r, c)])

    for cell in dead_cells:
        for c in Cell.cell_neighbour_8[cell[0]]:
            if c.state == State.alive.value:
                if not cell[0].is_edge:
                    cells_to_wall.append(cell[0])
                break
    set_state(cells_to_wall, State.rock.value)
    add_walls4(screen)
@time_func
def add_walls4(screen):
    Cell.wall3_num += 1
    dead_cells = []
    cells_to_wall = []

    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            cell = Cell.cell_grid[r][c]
            if cell.state == State.dead.value:
                dead_cells.append(cell)

    for cell in dead_cells:
        for c in Cell.cell_neighbour_4[cell]:
            if c.state == State.alive.value:
                cells_to_wall.append(c)
    set_state(cells_to_wall, State.rock.value)
@time_func
def clean_up(screen):
    Cell.clean_num += 1
    cells_to_kill = []
    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            cell = Cell.cell_grid[r][c]
            if not is_clean(cell, 1, Cell.cell_neighbour_8):
                cells_to_kill.append(cell)
    set_state(cells_to_kill, State.dead.value)
@time_func
def clean_up_bigger(screen):
    Cell.clean_bigger_num += 1
    cells_to_kill = []
    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            cell = Cell.cell_grid[r][c]
            if not is_clean(cell, 3, Cell.cell_neighbour_8):
                cells_to_kill.append(cell)

    set_state(cells_to_kill, State.dead.value)
@time_func
def clean_up_huge(screen):
    Cell.clean_huge_num += 1
    cells_to_kill = []
    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            cell = Cell.cell_grid[r][c]
            if not is_clean(cell, 4, Cell.cell_neighbour_8):
                cells_to_kill.append(cell)

    set_state(cells_to_kill, State.dead.value) 
@time_func
def randomise(screen):
    reset_info()
    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            cell = Cell.cell_grid[r][c]
            cell.state = State.dead.value if cell.is_edge else randint(State.dead.value, State.alive.value)   
@time_func
def iterate(screen):
    Cell.iteration_num += 1
    cells_to_change = get_cells_to_change(is_change_required, Cell.cell_neighbour_8)
    flip_state(cells_to_change)
@time_func
def iterate_new(screen):
    Cell.iteration_new_num += 1
    cells_to_change = get_cells_to_change(is_trip_required, Cell.cell_neighbour_8)
    flip_state(cells_to_change)
@time_func
def island_round(screen):
    Cell.island_round_num += 1
    cells_to_change = get_cells_to_change(is_change_big, Cell.cell_neighbour_20)
    flip_state(cells_to_change)
@time_func
def create_main_islands(screen):
    visited = get_island_visited_dict(Cell.cell_neighbour_8)
    islands = []
    for cell in Cell.cell_neighbour_8:
        if not visited[cell]:
            island = cc_while_dfs(cell, visited, Cell.cell_neighbour_8)
            islands.append(island)

    islands.sort(key = len)

    if len(islands) > 3:
    
        main = [
        islands.pop(),
        islands.pop(),
        islands.pop(),
        ]
        Cell.islands = main
        for island in islands:
            set_state(island, State.dead.value )
    else:
        Cell.islands = islands
@time_func
def find_lakes(screen):
    islands = []
    visited = get_lake_visited_dict(Cell.cell_neighbour_8)
    for cell in Cell.cell_neighbour_8:
        if not visited[cell]:
            island = cc_while_dfs(cell, visited, Cell.cell_neighbour_8)
            islands.append(island)

    islands.sort(key = len)
    islands.pop() ## assuming the biggest dead cell island is the sea
                  ## only works when the biggest dead island is the one surrounding the live islands
    for island in islands: 
        set_state(island, State.lake.value)
@time_func
def create_path(screen):
    for island in Cell.islands:
        start = get_random_cell_at_edge(island, Cell.cell_neighbour_4)
        distances = all_distances_from_cell(start, island, Cell.cell_neighbour_4)
        end, path = get_longest_path(distances, start)
        if len(path) > 8:
            set_state(path, State.path.value)
            start.draw('yellow')
            end.draw('red')
@time_func
def create_longest_path(screen):
    main_island = Cell.islands[0]
    # left, right, top, bottom = get_islands_extremes(main_island)
    edge = get_island_edge_cells(main_island, Cell.cell_neighbour_4)
    longest_path = []
    start = None
    finish = None
    print(len(edge))
    # for cell in edge:
    #     distances = all_distances_from_cell(cell, main_island, Cell.cell_neighbour_4)
    #     end, path = get_longest_path(distances, cell)
    #     if len(path) >= len(longest_path):
    #         start = cell
    #         end = finish
    #         longest_path = path
    set_state(longest_path, State.path.value)
@time_func
def create_territories(screen):
    # Cell.islands.sort()
    # main_island = Cell.islands.sort()
    # size = len(main_island)
    # territory_num = 4
    # territory_size = size // territory_num
    # start = get_random_cell_at_edge(main_island, Cell.cell_neighbour_4)
    pass
    



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
    island_round: 11,
    create_main_islands: 12,
    find_lakes: 13,
    create_path: 14,
    create_territories: 15,
    create_longest_path: 16,
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
    11: island_round,
    12: create_main_islands,
    13: find_lakes,
    14: create_path,
    15: create_territories,
    16: create_longest_path,
}