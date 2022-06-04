
from cell import *
from utils import time_func, disable
import copy
import queue
from collections import deque
from random import choice

#helper functions
def filter_cells(func, cell_dict):
    cells_to_change = []
    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            cell = Cell.cell_grid[r][c]
            if func(cell, cell_dict) and not cell.is_edge:
                cells_to_change.append(cell)
    return cells_to_change
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
    left = [Cell.column_num] 
    top = [Cell.row_num] 
    right = [-1] 
    bottom = [-1]
    for cell in island:
        if cell.state == State.alive.value:
            if cell.c <= left[0]: left = [cell.c, cell] 
            if cell.c >= right[0]: right = [cell.c, cell]
            if cell.r <= top[0]: top = [cell.r, cell]
            if cell.r >= bottom[0]: bottom = [cell.r, cell]
    return left, right, top, bottom
def generate_path_dicts(island):
    visited = {}
    distance = {}
    for cell in island:
        visited[cell] = False
        distance[cell] = []
    return visited, distance

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
def territory_dfs(cell, visited, cell_neighbour, territory_num, territory_size):
    stack = deque()
    stack.append(cell)
    territories = []
    colour_index = 0
    terr_cells = [cell]
    count = 0
    while len(stack) and count < territory_num:
        c = stack.pop()
        if not visited[c]:
            visited[c] = True
        for n in cell_neighbour[c]:
            if not visited[n] and n.state == State.alive.value:
                if len(terr_cells) == territory_size:
                    territory = {'cells' : copy.copy(terr_cells), 'colour':territory_colours[colour_index]}
                    territories.append(territory)
                    colour_index += 1
                    count += 1
                    terr_cells = []
                stack.append(n)
                terr_cells.append(n)
    return territories
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
    count = len(list(filter(lambda c : c.state == State.alive.value, 
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


# Generator functions
def add_walls(screen):
    cells_to_wall = filter_cells(is_wall, Cell.cell_neighbour_8)
    set_state(cells_to_wall, State.rock.value)
def add_walls2(screen):
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
def add_walls3(screen):
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
def add_walls4(screen):
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
def clean_up(screen):
    cells_to_kill = []
    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            cell = Cell.cell_grid[r][c]
            if not is_clean(cell, 1, Cell.cell_neighbour_8):
                cells_to_kill.append(cell)
    set_state(cells_to_kill, State.dead.value)
def clean_up_bigger(screen):
    cells_to_kill = []
    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            cell = Cell.cell_grid[r][c]
            if not is_clean(cell, 3, Cell.cell_neighbour_8):
                cells_to_kill.append(cell)

    set_state(cells_to_kill, State.dead.value)
def clean_up_huge(screen):
    cells_to_kill = []
    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            cell = Cell.cell_grid[r][c]
            if not is_clean(cell, 4, Cell.cell_neighbour_8):
                cells_to_kill.append(cell)

    set_state(cells_to_kill, State.dead.value) 
def randomise(screen):
    Cell.reset_info()
    for r in range(Cell.row_num):
        for c in range(Cell.column_num):
            cell = Cell.cell_grid[r][c]
            cell.state = State.dead.value if cell.is_edge else randint(State.dead.value, State.alive.value)   
def iterate(screen):
    cells_to_change = filter_cells(is_change_required, Cell.cell_neighbour_8)
    flip_state(cells_to_change)
def iterate_new(screen):
    cells_to_change = filter_cells(is_trip_required, Cell.cell_neighbour_8)
    flip_state(cells_to_change)
def island_round(screen):
    cells_to_change = filter_cells(is_change_big, Cell.cell_neighbour_20)
    flip_state(cells_to_change)
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
        main.sort(key = len)
        Cell.islands = main
        for island in islands:
            set_state(island, State.dead.value )
    else:
        Cell.islands = islands
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
def create_path(screen):
    for island in Cell.islands:
        start = get_random_cell_at_edge(island, Cell.cell_neighbour_4)
        distances = all_distances_from_cell(start, island, Cell.cell_neighbour_4)
        end, path = get_longest_path(distances, start)
        if len(path) > 8:
            set_state(path, State.path.value)
            start.draw('yellow')
            end.draw('red')
@disable
def create_territories(screen):
    screen.surface.fill('black')
    for point in Cell.points:
        pos = cartesian_to_screen(point[0], point[1], screen.current_height, screen.current_width)
        pygame.draw.circle(screen.surface, 'white', pos, 3, 2)
    pairs = get_point_pairs(screen, 3)
    for pair in pairs:
        a = pair[0]
        b = pair[1]
        mid_point = get_mid_point(a, b)
        screen_mid_point = cartesian_to_screen(mid_point[0], mid_point[1], screen.current_height, screen.current_width)
        perpendicular_slope = get_perpendicular_slope(a, b)
        start, end = get_edge_start_end(pair, screen, perpendicular_slope, mid_point)
        # smallest_x = - screen.current_width // 2
        # largest_x = screen.current_width // 2
        # cart_start = smallest_x, get_y(smallest_x, perpendicular_slope, mid_point)
        # cart_end = largest_x, get_y(largest_x, perpendicular_slope, mid_point)
        # start = cartesian_to_screen(smallest_x, get_y(smallest_x, perpendicular_slope, mid_point), screen.current_height, screen.current_width)
        # end = cartesian_to_screen(largest_x, get_y(largest_x, perpendicular_slope, mid_point), screen.current_height, screen.current_width)
        start = cartesian_to_screen(start[0], start[1], screen.current_height, screen.current_width)
        end  = cartesian_to_screen(end[0], end[1], screen.current_height, screen.current_width)
        pygame.draw.circle(screen.surface, 'purple', screen_mid_point, 3, 2)
        pygame.draw.line(screen.surface, 'purple', start, end)
@disable
def create_voronoi(screen):
    points = get_3_not_so_random_points(screen)
    
    pass
@disable
def remove_lone_wall(screen):
    for island in Cell.islands:
        edge = get_island_edge_cells(island, Cell.cell_neighbour_4)
        for cell in edge:
            surrounding_live_cells = list(filter(lambda c : c.state == State.alive.value, Cell.cell_neighbour_4[cell]))
            if len(surrounding_live_cells) <= 1:
                cell.state = State.dead.value
                surrounding_live_cells[0].state = State.rock.value


class Gen_func:
    def __init__(self):
        self.functions = []
        self.func_index = 0
    

    def add_func(self, func):
        self.functions.append(func)

    def create_func_dict(self):
        id_func = {}
        func_id = {}
        for func in self.functions:
            id_func[func.__name__] = func
            func_id[func] = func.__name__
        self.size = len(id_func)
        return id_func, func_id
    
    def handle_index_increase(self):
        next_i = self.func_index + 1
        if next_i < self.size:
            self.func_index = next_i
        Cell.draw_all()

    def handle_index_decrease(self):
        prev_i = self.func_index - 1
        if prev_i >= 0:
            self.func_index = prev_i
        Cell.draw_all()

    def get_current_func_name(self):
        return self.functions[self.func_index].__name__

    def display_current_command(self, screen):
        info = f'[ {self.get_current_func_name()} ]'
        pos_x = (screen.current_width // 2) - 100
        pos_y = 10
        display_info(info, pos_x, pos_y)


func_manager = Gen_func()
func_manager.add_func(add_walls)
func_manager.add_func(clean_up)
func_manager.add_func(clean_up_bigger)
func_manager.add_func(clean_up_huge)
func_manager.add_func(randomise)
func_manager.add_func(iterate)
func_manager.add_func(iterate_new)
func_manager.add_func(add_walls2)
func_manager.add_func(add_walls3)
func_manager.add_func(add_walls4)
func_manager.add_func(island_round)
func_manager.add_func(create_main_islands)
func_manager.add_func(find_lakes)
func_manager.add_func(create_path)
func_manager.add_func(create_territories)
func_manager.add_func(create_voronoi)
func_manager.add_func(remove_lone_wall)

id_func, func_id = func_manager.create_func_dict()